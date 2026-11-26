"""Build MIMIC pilot cases under the task-03 decisions (workspace CLAUDE.md, "Decisions" 1-19).

Same inputs as ``mimic_case_build.py`` (``02_source``, ``02_draft``, a manual file) plus the
condition rules of ``mimic_pilot_v3`` (``03_strict.csv``: core steps and the lab panels dropped by
the 50 % rule). What changes from task 02:

- reports carry findings + impression (decisions 6, 13): the radiology IMPRESSION is served with
  recommendations, notifications, hedged clinical inferences and references to later studies
  removed (``clean_impression``); note-extracted reports carry the reader's impression;
- ECG from MIMIC-IV-ECG machine measurements and machine report lines (1, 14);
- the non-contrast CT may be the explicit non-contrast part of a CTA report (2);
- telemetry from ICU heart-rhythm and ED rhythm records covering >= 12 h, else the note (5, 19);
  respiratory function from ICU NIF / vital capacity, else the note;
- the chief complaint is the reader's rewrite when triage holds a symptom label or nothing (7, 9);
- de-identification blanks that make a negation ambiguous are never served (16);
- knowledge-tool criteria are transferred and their library answer is accepted (17);
- avoided actions and prohibited recommendations are drafted only from documented facts (18).

No record content in this file (PhysioNet DUA).
"""

from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

import pandas as pd
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
for p in (ROOT / "agent-platform/src", ROOT / "packages/neuroagent-schemas/src", ROOT / "agent-platform/scripts/validation",
          ROOT / "data/review/round-2026-10/bin", HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from mimic_case_assemble import FINDINGS, anchor, hours, parse_medications, ts  # noqa: E402
from mimic_case_build import (_NORM, _WS, body_size, cut_hpi, drop_sentences, lab_rows, labs_output,  # noqa: E402
                              paragraphs, template_criterion, trajectory, verbatim, vitals)
from mimic_pilot_v3 import CTA_EXAM, MRI_EXAM, NCCT_EXAM, NONCONTRAST_IN_CTA, SPINE_MRI_EXAM, rhythm_hours  # noqa: E402

CONDITION_ENUM = {"SE": "status_epilepticus", "ISCH": "ischemic_stroke", "SAH": "subarachnoid_hemorrhage",
                  "GBS": "guillain_barre", "MS": "multiple_sclerosis", "FEPI": "focal_epilepsy_temporal"}
SYNONYM_CATEGORY = {"SE": "G41", "ISCH": "I63", "SAH": "I60", "GBS": "G61", "MS": "G35", "FEPI": "G40"}
ICD9_TO10 = {"SE": "G41.9", "ISCH": "I63.9", "SAH": "I60.9", "GBS": "G61.0", "MS": "G35", "FEPI": "G40.209"}
RECOMMENDED = {"SE": ["mri_brain"], "ISCH": ["echo", "cardiac_monitoring", "mri_brain"], "SAH": ["csf"],
               "GBS": ["mri_brain", "body:spine_MRI"], "MS": ["csf"], "FEPI": []}
KNOWLEDGE = {"knowledge:check_drug_interactions": "check_drug_interactions",
             "knowledge:search_medical_literature": "search_medical_literature"}

_SPLIT = re.compile(r"(?<!\be\.g)(?<!\bi\.e)(?<!\bvs)(?<!\bDr)(?<!\bapprox)(?<!\bca)(?<=[.;])\s+")


def split_sents(t: str) -> list[str]:
    """Sentence split that does not break at e.g., i.e., vs., Dr., approx."""
    return _SPLIT.split(t or "")


# --- de-identification blanks that hide a negation (decision 16) -------------------------------
_BLANK_AT = re.compile(r"___\s+(?=[A-Za-z])")
# Words after which a blank is a de-identified name, date, place or age, not a lost negation.
_SAFE_BEFORE = re.compile(r"(?i)(?:\b(?:on|at|in|to|from|of|by|dr|mr|mrs|ms|miss|a|an|the|per|via|since|until|into|for|patient|pt|age|aged|"
                          r"name|is a|was a|old|year|years|admitted|discharged|transferred|seen|called|told|with dr)\.?|\d)\s*$")
_SAFE_AFTER = re.compile(r"(?i)(?:year|yo\b|y/o|y\.o|-year|years|M\b|F\b|male|female|man\b|woman\b|Hospital|hospital|ED\b|clinic|Clinic|"
                         r"Center|center|Medical|Rehab|rehab|Nursing|nursing|Health|health|Street|St\b|Ave|MD\b|NP\b|PA\b|RN\b|Unit|unit|"
                         r"at\b|in\b|on\b|of\b|to\b|from\b|and\b|or\b|___|am\b|pm\b|AM\b|PM\b|hours?\b|days?\b|weeks?\b|months?\b|"
                         r"times?\b|mg\b|syndrome|disease|criteria|sign\b|test\b|scale|Scale|score|Stroke|stroke|is\b|was\b|has\b|had\b|"
                         r"reports?\b|states?\b|stated|presented|presents|says|said|notes?\b|denies|endorses|who\b|'s\b)")


# A blank hides a negation when the words after it are a clinical finding that is normally negated
# ("___ edema", "___ bruits", "There is ___ aortic stenosis", "___ Known Allergies"); a blank before a
# number, a name, a date, an age or a place is ordinary de-identification and is kept.
_NEGATABLE = re.compile(
    r"(?i)(?:known\s+allerg|evidence|(?:acute|focal|significant|definite|obvious|apparent|gross|clear|new|further|other|prior|"
    r"recent)\b|edema|bruits?|murmurs?|m/r/g|r/r/w|rubs?|gallops?|distress|tremor|asterixis|apraxia|dyspraxia|paraphasic|"
    r"drooling|slurred|difficulty|dysarthria|aphasia|neglect|nystagmus|ptosis|deficits?|weakness|numbness|tingling|pain|"
    r"headache|fevers?|chills|nausea|vomiting|seizures?|lesions?|masses|mass\b|thromb|vegetation|effusion|pericardial|"
    r"atrial\s+septal|ventricular\s+septal|aortic|mitral|tricuspid|pulmonic|valv|stenosis|regurgitation|PFO|ASD\b|VSD\b|"
    r"hemorrhag|bleed|infarct|fracture|abnormalit|family\s+history|history\s+of|changes?\b|clubbing|cyanosis|rash|"
    r"lymphadenopathy|LAD\b|JVD|organomegaly|tenderness|rigidity|meningism|clonus|babinski|fasciculation|drift|"
    r"incontinence|retention|loss\s+of|improvement|response|relief|symptoms?)")


class _Blank:
    """A de-identification blank that hides a negation (decision 16)."""

    @staticmethod
    def findall(text: str) -> list[str]:
        hits = []
        for m in _BLANK_AT.finditer(text or ""):
            after = text[m.end():m.end() + 40]
            if _SAFE_AFTER.match(after) or not _NEGATABLE.match(after):
                continue
            hits.append(m.group(0))
        return hits

    def search(self, text: str) -> bool:
        return bool(self.findall(text))


_BLANK = _Blank()


def ambiguous_blanks(text: str) -> int:
    return len(_BLANK.findall(text or ""))


OPTS = {"treatments": "04_treatments.parquet", "eeg_strip_treatment": True, "grid_mode": "drop"}  # task 06 switches
TAG = ["03"]  # output prefix: 03 (task 03) or 04 (task 04)
DROPPED: list[str] = []  # every sentence or fragment dropped for an ambiguous blank, per case (audit)


def drop_ambiguous(text: str) -> tuple[str, int]:
    """Drop every sentence that holds an ambiguous blank."""
    out, n = [], 0
    for sent in re.split(r"(?<!\bMr)(?<!\bMs)(?<!\bDr)(?<!\bMrs)(?<!\bSt)(?<=[.;!?])\s+|\n", text or ""):
        if _BLANK.search(sent):
            n += 1
            DROPPED.append(_WS(sent))
            continue
        out.append(sent)
    return _WS(" ".join(out)), n


GRID_CELLS = None  # set by mimic_case_build6 (decision 35)


def drop_blank_grids(value: str) -> tuple[str, int]:
    """Decision 27: a strength or reflex grid holding a de-identification blank (a lost value or column name) is not served."""
    parts, n, header_dropped = [], 0, False
    for frag in (value or "").split(" | "):
        toks = frag.split()
        grades = sum(bool(re.fullmatch(r"\d[+-]?|\d\+?/\d|___-?|NT|tr|0", t)) for t in toks)
        abbrevs = sum(bool(re.fullmatch(r"[A-Z][A-Za-z]{1,4}\.?", t)) for t in toks)
        grade_row = grades >= 3 and grades >= len(toks) - 2
        if ("___" in frag and (grades >= 4 or abbrevs >= 3)) or (header_dropped and grade_row):
            n += 1
            header_dropped = header_dropped or abbrevs >= 3
            DROPPED.append("[grid with blank] " + _WS(frag)[:120])
            continue
        header_dropped = False
        parts.append(frag)
    return " | ".join(parts), n


def drop_ambiguous_fragments(value: str) -> tuple[str, int]:
    """Exam / PMH style values: drop the ' | '-separated fragment or sentence holding a blank."""
    parts, n = [], 0
    hdr_tok = re.compile(r"^(?:\[?\(?[A-Z][A-Za-z/]{0,8}\.?\)?\]?|\[?___\]?|[A-Z]{1,3}\d?(?:-[A-Z]?\d)?)$")
    for frag in value.split(" | "):
        toks = frag.split()
        if len(toks) >= 4 and sum(bool(hdr_tok.match(t)) for t in toks) == len(toks):
            parts.append(frag)  # task 07: a grid header with a blanked column name hides no negation (decision 35 serves the named columns)
            continue
        kept, k = drop_ambiguous(frag)
        n += k
        if kept:
            parts.append(kept)
    return " | ".join(parts), n


# --- reports: findings + impression (decisions 6, 13) -------------------------------------------
IMPRESSION = re.compile(r"(?is)(?:\b(?:IMPRESSIONS?|CONCLUSIONS?)\s*:|(?<=\n)(?-i:[ \t]*(?:IMPRESSIONS?|CONCLUSIONS?))[ \t]*\n)(.*?)(?=\n\s*(?:(?:MRI?|MR|CT)\s+OF\s+THE\s+[A-Z ]*SPINE\s*:|NOTIFICATION|RECOMMENDATION\(S\)|ADDENDUM|ATTENDING|"
                        r"DR\.|I have personally|The study and the report)\b|\Z)")
_IMP_DROP = re.compile(
    r"recommend|(?<!\bto )(?<!\bto\s\s)\bsuggest(?:ed|s)?\b|\bsuggestion\b(?!\s+of\b)|advis|(?:clinical(?:ly)?\s+)correlat\w*|correlat\w*\s+(?:clinically|with (?:clinical|the clinical|history|symptoms|exam|conv\w*|conventional|catheter|angio\w*|dsa|lab\w*|laboratory|csf|(?:a\s+)?(?:\w+\s+)?(?:ultrasound|US\b|imaging|MRI|CT\b|exam\w*)))|correlation (?:is |would be )?(?:recommended|advised|suggested|needed)|follow[- ]?up|could be (?:obtained|performed|considered)|if (?:clinically|there is|further)|"
    r"\bconsider\b|would be (?:helpful|useful)|is more sensitive|further evaluation|discussed|communicated|notified|paged|"
    r"telephone|by phone|called|e-?mail|at the time of (?:the )?(?:study|dictation)|findings were|wet read|"
    r"given (?:the )?(?:patient'?s )?(?:clinical )?history|in the (?:clinical )?setting of|clinical (?:history|context)|"
    r"subsequent|later study|follow-up study|diagnostic considerations?|differential|could also include|"
    r"in an appropriate clinical setting|clinical significance|of doubtful clinical|clinically significant|may be (?:helpful|obtained|considered)|"
    r"can be obtained|should be obtained|is suggested|correlate clinically|helpful|is recommended|are recommended", re.I)
_IMP_CLAUSE = re.compile(r"(?i),?\s*(?:which (?:is|are) )?(?:non-?specific,?\s*(?:though|but)\s*)?"
                         r"(?:compatible|consistent) with (?:the )?clinical (?:suspicion|history|concern|diagnosis)(?: of)?[^.;]*")
_STUB = re.compile(r"(?:(?<=\s)|^)\d+[.)]\s*(?=(?:\d+[.)]\s)|$)")


def tidy_impression(text: str) -> str:
    """Remove empty item numbers left by dropped items ('2. 3. 4. X' -> '4. X')."""
    prev = None
    while prev != text:
        prev, text = text, _STUB.sub("", text)
    return re.sub(r";\s*$", ".", re.sub(r"\.\.+(?=\s|$)", ".", _WS(text)))


# Clauses that leave the image: the clinical diagnosis or mechanism the report infers from outside it.
_IMP_CLINICAL = re.compile(
    r"(?i),?\s*(?:which (?:is|are|may be) |and )?(?:most )?(?:likely |possibly |probably )?(?:compatible|consistent|in keeping|suggestive|concerning|"
    r"worrisome)\s+(?:with|for)\s+(?:a |an |the )?(?:known |clinical |history of )?(?:multiple sclerosis|\bMS\b|"
    r"neuromyelitis|\bNMO|\bADEM\b|guillain|\bGBS\b|vasculitis|embolic (?:etiology|source|mechanism|phenomen\w*|disease)|cardioembolic|"
    r"(?:an )?(?:active|progressive) disease|disease (?:activity|progression))[^.;]*")
_REC_CUT = re.compile(r"(?i)[,;]?\s*(?:and\s+)?(?:\brecommend\w*|(?<!\bto )(?<!\bto\s\s)\bsuggest(?:ed|s|ion)?\b|\badvis\w*|\bconsider\b|could be|would be|may be (?:helpful|obtained|considered)|"
                      r"can be obtained|should be obtained|is suggested|if (?:clinically|there is|further)|"
                      r"\b(?:clinical(?:ly)?\s+)correlat\w*|\bcorrelat\w*\s+(?:clinically|with (?:clinical|the clinical|history|symptoms|exam))|follow[- ]?up|further evaluation|discussed|communicated|notified|was paged|by phone|preliminary)\b.*$")
_LATER = re.compile(r"(?i)\bsubsequent\b|\blater (?:MR|MRI|CT|study|exam)|\bfollow-?up (?:MR|MRI|CT|study|exam)\b|"
                    r"\bbetter (?:assessed|evaluated|seen) on (?:the )?(?:subsequent|following|later)")
_RESULT_COMM = re.compile(r"(?i)\bpreliminary\b|reviewed with|wet read|high risk:|low risk|CT in .{0,12}months|months and then|discrepanc|attending (?:review|radiologist)|resident|"
                          r"discussed with|communicated (?:to|with|by)|telephone|"
                          r"paged|were (?:conveyed|reported) to|at the time of (?:the )?(?:study|dictation|discovery)|findings were|"
                          r"by dr\.|nodule.{0,60}(?:fleischner|follow-?up)|fleischner|annual (?:screening|follow)|"
                          r"prevalence|incidental(?:ly)? (?:noted )?(?:pulmonary|lung) nodule|"
                          r"\((?:neurology|stroke|neurosurgery|ED|emergency|medicine|ICU|primary) team\)|\b(?:neurology|stroke|neurosurgery|ED|primary) team\b|"
                          r"\bat \d{1,2}(?::\d{2})?\s*(?:AM|PM|a\.m\.|p\.m\.)|(?:high|low)[- ]risk patients?|"
                          r"\bon ___ at\b|\bwas (?:informed|notified|told)\b|\bvia (?:phone|telephone|page)|\bphone call\b|\bin-person\b|"
                          r"\bat (?:roughly |approximately |about )?\d{3,4} hours\b|discovery of the findings|after the discovery|"
                          r"guideline|society|^\s*COMMENT:|^\s*dedicated\b.{0,80}\b(?:imaging|MRI|MR|CT|CTA|study|evaluation)\b|"
                          r"\bhas been\s*[.;]?\s*$")


# Inferences that use information outside the image (another study, the history, the clinical picture).
_INFERENCE = re.compile(
    r"(?i),?\s*(?:which,?\s*)?(?:in conjunction with|particularly (?:given|as)|given (?:the )?(?:findings|history|clinical)|"
    r"in the setting of (?:the )?(?:patient|known|clinical|reported)|"
    r"(?:are |is )?(?:concerning|suspicious|worrisome|suggestive)\s+for\s+(?:a\s+)?(?:new\s+diagnosis\s+of\s+)?(?:multiple sclerosis|\bMS\b)|"
    r"such as multiple sclerosis|(?:are |is )?presumed (?:to be )?(?:embolic|cardioembolic)|"
    r"(?:in keeping|consistent|compatible|in accordance|correlat\w*)\s+with\s+(?:the\s+)?(?:patient'?s\s+)?(?:known\s+|prior\s+|reported\s+)?(?:history|diagnosis|clinical)|"
    r"(?:could|may|might) represent [^.;]*?(?:status epilepticus|seizure|ictal|demyelinat))[^.;]*")


_D24_PATTERN = re.compile(r"(?i)^\s*(?:\d+[.)]\s*)?(?:these\s+|the\s+)?(?:findings?|appearance)\s+(?:are\s+|is\s+)?(?:most\s+)?(?:consistent|compatible|in keeping|suspicious)\s+"
                          r"(?:with|for)\s+(?:known\s+)?(?:multiple sclerosis|MS)\s*,?\s*with\s+([^.;]+?)(?:\s*,?\s+given\s+[^.;]*)?\s*[.;]?\s*$")


def clean_sentence(x: str) -> str:
    """Keep the finding of a sentence, cut the recommendation / communication / clinical-diagnosis tail."""
    m = _D24_PATTERN.match(x)
    if m and len(m.group(1).split()) >= 2:  # decision 24: the disease name goes, the pattern (and the report's own hedge) stays
        D24["pattern_rewritten"] += 1
        x = re.sub(r"(?i)\s*(?:known\s+)?(?:multiple sclerosis|\bMS\b)\s*,?\s*with\s+", " ", x, count=1).strip()
        x = re.sub(r"\s+", " ", x)
    orig = x
    x = re.sub(r"(?i),?\s*(?:but|and|although)?\s*the clinical significance of (?:this|these|the) (?:finding|findings)?\s*(?:is|are) (?:uncertain|unclear|unknown|indeterminate)", "", x)
    x = re.sub(r"(?i),?\s*(?:that|which)?\s*(?:is|are)?\s*(?:better|more fully|further)\s+(?:evaluated|assessed|seen|characterized|"
               r"demonstrated)\s+on\s+(?:the\s+)?(?:subsequent|following|later)[^.;]*", "", x)
    if _RESULT_COMM.search(x) or _LATER.search(x):
        return ""
    x = _IMP_CLAUSE.sub("", x)
    x = _IMP_CLINICAL.sub("", x)
    x = _INFERENCE.sub("", x)
    x = re.sub(r"(?i),?\s*(?:most\s+)?(?:likely|probably|possibly|presumably)\s+(?:of\s+)?(?:embolic|cardioembolic|thromboembolic)(?:\s+(?:etiology|origin|source|in nature))?\b[^.;]*", "", x)
    if re.search(r"(?i)\b(?:is|are)\s+suggested\s+(?:in|at|on|within|along|over|involving)\b", x):
        TXCOUNT["hedged_finding_sentence_dropped"] += 1
        return ""  # "a lesion is suggested in ..." is a hedge, not a recommendation: cutting it would assert the lesion
    x2 = re.sub(r"(?i)[,;]\s*(?:and\s+)?(?:close\s+)?attention\s+(?:in|on|to|at)\b[^.;]*?\b(?:is|are)\s+(?:also\s+)?(?:advised|recommended|suggested)", "", x)
    if x2 != x:
        TXCOUNT["followup_attention_clause_cut"] += 1
        x = x2
    if _IMP_DROP.search(x):
        head = _REC_CUT.sub("", x)
        if len(re.findall(r"[A-Za-z]{3,}", head)) >= 3 and not _IMP_DROP.search(head):
            x = head
        else:
            return ""
    x = strip_disease(x)
    x = repair_fragment(x, orig)
    if x != "" and x != orig and len(re.findall(r"[A-Za-z]{3,}", x)) < 2:
        return ""  # a cut left nothing of the finding (an untouched short sentence, "No hemorrhage.", stays)
    return x


_VERB = re.compile(r"(?i)\b(?:is|are|was|were|has|have|had|be|been|shows?|showed|demonstrat\w*|seen|noted|identified|present|appears?|"
                   r"measur\w*|extends?|extending|involv\w*|remains?|unchanged|stable|consistent|compatible|suggest\w*|represent\w*|reflect\w*|"
                   r"no|without|evidence|there|courses?|runs?|lies|contacts?|abuts?|loops?|crosses|arises?|terminates?|enhances?|occupies)\b")
_ORPHAN = re.compile(r"^\s*(?:[a-z(]|(?i:however|but|although|these|this|it|they|which|and|or|note that|also|additional|additionally|otherwise)\b)")


def orphan_rule(items: list[str], kept: list[str]) -> list[str]:
    """A piece that only continues a removed piece ("...; neoplasm less likely", "However, ...") goes with it."""
    out = []
    for i, (a, b) in enumerate(zip(items, kept)):
        prev_changed = i > 0 and items[i - 1] != out[i - 1]  # a piece dropped as an orphan counts as dropped
        if b and prev_changed and _ORPHAN.match(b) and not re.match(r"^\s*(?:no|there)\b", b, re.I):
            TXCOUNT["orphan_piece_dropped"] += 1
            b = ""
        out.append(b)
    return out


_DANGLING = re.compile(r"(?i)[,;:]?\s*\b(?:but|and|or|which|that|though|although|however|while|whereas|with|of|for|to|as|is|are|was|were|"
                       r"could|may|might|can|would|will|be|likely|possibly|probably|most|more|less|than|the|a|an|in|on|by|"
                       r"represent|represents|reflect|reflects|suggest|suggests|suggesting|indicat\w*|raising|concerning|"
                       r"compatible|consistent|in keeping|appearance is|this is|this|these|which is|which are|highly|strongly|very|distribution|there|there is|there are)\s*[.;,]?\s*$")


def repair_fragment(x: str, orig: str) -> str:
    """A cut that leaves a dangling word ('nonspecific, but.', 'This appearance is.') is closed at the last
    complete phrase; a conditional or a clause whose main part was cut ('If these findings represent ...',
    'Equivocal abnormality could.') is dropped."""
    if not x or x == orig:
        return x
    y = x.rstrip()
    end = "." if not y.endswith(";") else ";"
    y = y.rstrip(" .;")
    prev = None
    while prev != y:
        prev, y = y, _DANGLING.sub("", y).rstrip(" ,;:")
    if re.match(r"(?i)\s*(?:if|although|though|while|whereas|unless|when)\b", y) or len(re.findall(r"[A-Za-z]{3,}", y)) < 2:
        return ""
    if _VERB.search(orig) and not _VERB.search(y):  # the cut took the verb: a fragment, not a finding
        if len(re.findall(r"[A-Za-z]{3,}", y)) >= 5 and not re.match(r"(?i)\s*(?:the|this|these|its|that)\b", y):  # task 06: a complete noun phrase ("Several white matter lesions in ...") is a finding
            TXCOUNT["verbless_noun_phrase_kept"] += 1
            return y + end
        TXCOUNT["verbless_fragment_dropped"] += 1
        return ""
    return y + end


# --- decision 24: disease or syndrome names a study alone cannot establish ------------------------
_DISEASE = (r"multiple\s+sclerosis|(?-i:\bMS\b)(?!\s*(?:sequence|imaging))|guillain[- ]?barr[eé]|\bGBS\b|miller[- ]?fisher|\bAIDP\b|"
            r"\bAMAN\b|\bAMSAN\b|\bCIDP\b|vasculitis|neuromyelitis(?:\s+optica)?|\bNMO(?:SD)?\b|\bADEM\b|neuro-?sarcoid\w*|"
            r"\bsarcoid\w*|\blupus\b|\bSLE\b|lyme|susac|bal[oó]'?s?\b")
_DISEASE_RX = re.compile(r"(?i)" + _DISEASE)
_BALO = re.compile(r"(?i)\bbal[oó]'?s?\b(?:[- ](?:like|type))?(?:\s+(?:concentric\s+sclerosis|type|lesions?|pattern))?(?:[- ]like)?")
_DISEASE_CLAUSE = re.compile(
    r"(?i)[,;]?\s*(?:(?:which|that) (?:is|are|may be|could be|likely represents?|represents?) |and |or )?(?:most |more )?(?:likely |possibly |probably )?"
    r"(?:(?:which|that)\s+(?:may |might |could |likely |probably )?(?:represents?|reflects?|indicates?)|compatible|consistent|in keeping|suggestive|typical|characteristic|concerning|worrisome|c/w|related|due|attributable|secondary|"
    r"sequela[e]?|in (?:this|a|the) (?:patient|setting|context))\s*(?:with|of|for|to)?\s+(?:[\w'’/-]+\s+){0,6}?(?:" + _DISEASE + r")[^.;]*")
_BALO_CLAUSE = re.compile(r"(?i)[,;]?\s*(?:(?:which|that) (?:is|are|may be) )?(?:most )?(?:likely )?(?:compatible|consistent|in keeping|suggestive|"
                          r"typical|characteristic|concerning)\s+(?:with|of|for)\s+(?:a |an |the )?bal[oó]'?s?\b[^.;]*")
D24 = collections.Counter()


def strip_disease(x: str) -> str:
    """Decision 24: serve the pattern a study shows, never a disease or syndrome name it cannot establish."""
    if not _DISEASE_RX.search(x or ""):
        return x
    y = _BALO_CLAUSE.sub("", x)
    if not re.search(r"(?i)concentric|ring|lamellat|onion", y):
        y = _BALO.sub("concentric ring lesion", y)
    else:
        y = _BALO.sub("", y)
    if y != x:
        D24["balo_rewritten"] += 1
    if not _DISEASE_RX.search(y):
        return y
    z = _DISEASE_CLAUSE.sub("", y)
    if z != y and not _DISEASE_RX.search(z) and len(re.findall(r"[A-Za-z]{3,}", z)) >= 2:
        D24["clause_cut"] += 1
        return z if re.search(r"[.;]\s*$", z) or not re.search(r"[.;]\s*$", y) else z
    D24["sentence_dropped"] += 1
    return ""


def strip_disease_text(t: str) -> str:
    parts = []
    for p in re.split(r"(\n\s*\n)", t or ""):
        if re.fullmatch(r"\n\s*\n", p):
            parts.append(p)
            continue
        parts.append(" ".join(y for y in (strip_disease(s) for s in split_sents(p)) if y))
    return "".join(parts).strip()


# --- decision 27: a de-identification blank where a value stands ------------------------------
_UNIT = r"(?:%|mm\b|cm\b|mg|g/dl|ms\b|bpm|mmhg|cells|/mm|x\s?10|units?\b|ml\b|sec\b|hz\b|uv\b|m/s|mv\b|#/ul)"
_VALUE_BLANK = re.compile(r"(?i)(?:[:=]\s*|[<>]\s*)___(?=\s*(?:" + _UNIT + r"|[.,;)]|$))|___\s*" + _UNIT)
D27 = collections.Counter()


def drop_value_blanks(t: str) -> str:
    if not isinstance(t, str) or "___" not in t:
        return t
    out = []
    for s in split_sents(t):
        if _VALUE_BLANK.search(s):
            D27["sentences_dropped"] += 1
            DROPPED.append("[value blank] " + _WS(s))
            continue
        if "___" in s and len(re.findall(r"[A-Za-z]{3,}", s.replace("___", " "))) < 3:
            D27["blank_only_fragments_dropped"] += 1
            DROPPED.append("[blank-only fragment] " + _WS(s))
            continue
        out.append(s)
    return " ".join(out)


_EEG_TX = re.compile(r"(?i)[,;]?\s*(?:\(|\b(?:or|and)\s+)?(?:(?:which|that) (?:is|are|may be|can be) )?(?:most |more )?(?:likely |possibly |probably )?"
                     r"(?:(?:consistent with|suggestive of|due to|related to|from|reflecting|can be seen with|seen with|attributable to)\s+)?"
                     r"(?:an?\s+)?(?:the\s+)?(?:anesthetic|anaesthetic|sedative|sedation|medication|medications|drug|benzodiazepine|propofol|midazolam|"
                     r"ketamine|pentobarbital|barbiturate)s?(?:\s+(?:medication|infusion|administration))?(?:\s+effects?)?\)?(?=[\s.,;)]|$)")


def strip_eeg_treatment(t: str) -> str:
    """EEG text that reveals the treatment (medication or anaesthetic effect, burst suppression) is not served."""
    if not isinstance(t, str):
        return t
    out = []
    for x in split_sents(t):
        if re.search(r"(?i)burst[- ]?suppress", x):
            TXCOUNT["eeg_burst_suppression_sentence_dropped"] += 1
            continue
        y = _EEG_TX.sub("", x)
        if y != x:
            TXCOUNT["eeg_treatment_clause_cut"] += 1
            y = re.sub(r"\(\s*\)", "", y)
            while y.count("(") > y.count(")"):  # a cut inside "( ... or medication effect)" leaves an open parenthesis
                i = y.rfind("(")
                y = y[:i].rstrip() + ", " + y[i + 1:].lstrip()
            y = re.sub(r"\s+([,.;)])", r"\1", y).strip()
            if len(re.findall(r"[A-Za-z]{3,}", y)) < 2:
                continue
        out.append(y)
    return " ".join(out)


_PROV = r"(?:the |this )?(?:discharge )?(?:note|hospital[- ]course|discharge summary|narrative|pertinent results|extracted|extraction)\b"
_PROV_PAREN = re.compile(r"(?i)\s*\([^()]*\b" + _PROV + r"[^()]*\)")
_PROV_SENT = re.compile(r"(?i)\b" + _PROV)


def strip_provenance(t: str) -> str:
    """Note-extracted outputs never say where they were taken from (that is hidden metadata)."""
    if not isinstance(t, str):
        return t
    y = _PROV_PAREN.sub("", t)
    if y != t:
        TXCOUNT["provenance_parenthesis_removed"] += 1
    out = []
    for x in split_sents(y):
        if _PROV_SENT.search(x):
            TXCOUNT["provenance_sentence_removed"] += 1
            continue
        out.append(x)
    return " ".join(out).strip()


def walk_strings(o, f):
    if isinstance(o, str):
        return f(o)
    if isinstance(o, list):
        return [y for y in (walk_strings(x, f) for x in o) if y not in ("", None)]
    if isinstance(o, dict):
        return {k: (walk_strings(v, f) if not k.startswith("_") and k not in ("eeg_type", "test_type", "echo_type", "monitor_type") else v)
                for k, v in o.items()}
    return o


def clean_impression(report: str) -> tuple[str, int, int]:
    """The IMPRESSION section with what decision 6 / 13 removes taken out (clause level where possible)."""
    m = IMPRESSION.search(report or "")
    if not m:
        return "", 0, 0
    items = [x for x in re.split(r"(?<=[.;])\s+|\n\s*(?=\d+[.)]\s)", _WS(m.group(1))) if x.strip()]
    kept = orphan_rule(items, [clean_sentence(x) for x in items])
    dropped = sum(1 for a, b in zip(items, kept) if a != b)
    kept = [x if re.search(r"[.;]\s*$", x) else x + "." for x in kept if _WS(x).strip(" .;") and re.search(r"[A-Za-z]{3,}", x)]
    return tidy_impression(" ".join(kept)), len(items), dropped


_VESSEL = re.compile(r"(?i)arter|\bICA\b|\bMCA\b|\bACA\b|\bPCA\b|\bM[1-4]\b|\bA[12]\b|\bP[12]\b|vertebr|basilar|carotid|"
                     r"aneurysm|stenos|occlusi|occlud\w*|\bV[1-4]\b|reconstitut\w*|dissect|thromb|\bCTA\b|angiogra|perfusion|vessel|opacification|flow|circle of willis|"
                     r"venous|dural sinus|sagittal sinus|transverse sinus|sigmoid sinus")
# A vascular territory names where a parenchymal finding lies ("PCA territory infarct"): not a vessel finding.
_TERRITORY = re.compile(r"(?i)\b(?:MCA|ACA|PCA|ICA|PICA|AICA|SCA|anterior|middle|posterior)(?:\s*/?\s*(?:MCA|ACA|PCA))?(?:\s+cerebral)?(?:\s+artery)?\s+(?:external\s+cortical\s+)?(?:vascular\s+)?(?:territor\w*|border-?\s?zone|watershed|distribution)|watershed|border-?\s?zone|small vessel|"
                       r"(?:territory|distribution)\s+of\s+the\s+(?:left\s+|right\s+)?(?:middle|anterior|posterior)\s+cerebral\s+arter(?:y|ies)")


class _VesselTest:
    def __init__(self, nc: bool = False):
        self.nc = nc

    def search(self, text: str):
        if self.nc and re.search(r"(?i)hyperdens|dense (?:MCA|artery|vessel)|(?<!non-)(?<!non)calcif", text or "") \
                and not re.search(r"(?i)stenos|occlu|opacif|thromb|aneurysm|dissect|atherom|atheroscl|narrow", text or ""):
            return None  # task 06/07: in a plain-CT answer a hyperdense vessel or vascular calcification is a non-contrast finding
        return _VESSEL.search(_TERRITORY.sub(" ", text or ""))


VESSEL = _VesselTest()
VESSEL_NC = _VesselTest(nc=True)  # used only where the plain-CT part is filtered


_NOT_HEAD = re.compile(r"(?i)lung|apex|apical|pulmonar|thyroid|nodule|\bneck\b|cervical|mediastin|chest|esophag|trache|pleura|"
                       r"azygos|jugular|\bC[1-7]\b|C[1-7]-C?[1-7]|pedicle|odontoid|\bdens\b|atlanto|prevertebral|lymph node|vertebral body|"
                       r"emphysem|consolidat|aort|subclavian|supraclavicular|coronary|\bCABG\b|lingula|(?:right|left) (?:upper|middle|lower) lobe|bronch|atelecta")
_OTHER_STUDY = {"ct": re.compile(r"(?i)\bCTA\b|angiogra|perfusion|\bMRI?\b(?! compatible)|\bMRA\b"),
                "mri": re.compile(r"(?i)\bMRA\b|\bMRV\b|angiogra|venogra|\bCTA\b")}


_XREF_CLAUSE = re.compile(r"(?i),?\s*(?:which\s+)?(?:most\s+)?(?:probably|likely|possibly)?\s*(?:corresponds?|correlates?|corresponding|correlating)\s+(?:with|to)\s+[^.;]*"
                          r"|,?\s*(?:as\s+)?(?:seen|demonstrated|shown|better seen|better evaluated|evaluated)\s+on\s+(?:the\s+)?(?:concurrent\s+|same[- ]day\s+)?(?:CTA|CT angiogra\w*|perfusion|MRA|MRI)[^.;]*")


def no_other_study(t: str, kind: str) -> str:
    """Drop sentences of one study's answer that report or refer to another study of the same session (decision 2);
    task 06: a finding of this study that only points to the other study keeps its finding, the pointer clause goes."""
    xs = []
    for x in split_sents(t or ""):
        if _OTHER_STUDY[kind].search(x):
            y = _XREF_CLAUSE.sub("", x).rstrip(" ,;.")
            if y != x.rstrip(" ,;.") and not _OTHER_STUDY[kind].search(y) and len(re.findall(r"[A-Za-z]{3,}", y)) >= 3:
                TXCOUNT["other_study_clause_cut_finding_kept"] += 1
                x = y + "."
        xs.append(x)
    t = " ".join(xs)
    return filter_sents(t, lambda x: _OTHER_STUDY[kind].search(x) and not re.search(r"(?i)\b(?:prior|previous|earlier|outside|compar\w*|since|unchanged|stable|dated|ago)\b|from ___", x),
                        f"{kind}_other_study_sentence_dropped")


# What only a contrast or perfusion acquisition shows: never in the plain-CT answer.
_CONTRAST_ONLY = re.compile(r"(?i)hypervascular|\benhanc\w*|hyperemi|blood volume|mean transit|\bCBF\b|\bCBV\b|\bMTT\b|\bTmax\b|"
                            r"opacif|contrast blush|spot sign")


def split_cta(findings: str, impression: str) -> tuple[str, str, str]:
    """Explicit non-contrast part of a CTA report (decision 2): (non-contrast findings, its impression,
    the rest of the findings, which answer the angiography order)."""
    paras = [p for p in re.split(r"\n\s*\n", findings) if p.strip()]
    nc, rest, in_nc = [], [], False
    head = re.compile(r"(?im)^\s*(?:NON-?\s?CONTRAST|NONCONTRAST|UNENHANCED|NON-?ENHANCED|PRE-?CONTRAST|"
                      r"(?:HEAD\s+CT|CT\s+HEAD|CT\s+OF\s+THE\s+HEAD|HEAD)\s+(?:WITHOUT|W/O)\s+(?:IV\s+)?CONTRAST)[^:\n]{0,40}:")
    other = re.compile(r"(?im)^\s*(?:CTA|CT\s+ANGIO|CT\s+PERFUSION|PERFUSION|HEAD\s+CTA|NECK\s+CTA|CTA\s+(?:OF\s+THE\s+)?(?:HEAD|NECK))[^:\n]{0,40}:")
    lead = re.compile(r"(?i)^\s*(?:FINDINGS?\s*:\s*)?(?:The\s+)?(?:pre-?\s?contrast|non-?\s?contrast|noncontrast|unenhanced|non-?enhanced)\s+"
                      r"(?:images?|scan|study|portion|series|(?:head\s+)?CT)\b")  # task 07: a paragraph that opens on the non-contrast images
    for p in paras:
        if not head.search(p) and lead.match(p):
            nc.append(p)  # that paragraph only: the next one has no header to end it
            in_nc = False
            continue
        if head.search(p):
            in_nc = True
        elif other.search(p):
            in_nc = False
        (nc if in_nc else rest).append(p)
    if not nc:  # statements about the non-contrast images inside other paragraphs
        stm = re.compile(r"(?i)\b(?:on|in)\s+the\s+(?:non-?\s?contrast|noncontrast|unenhanced|non-?enhanced|pre-?contrast)\s+"
                         r"(?:images?|portion|scan|head\s+CT|CT|study|sequence)")
        for p in paras:
            for s in split_sents(p):
                if stm.search(s):
                    nc.append(s)
    # task 06: sections run together in one paragraph: the non-contrast part stops at the first CTA / perfusion header
    nc_text = "\n\n".join(nc)
    cut = re.search(r"(?i)\b(?:CTA|CT ANGIO\w*|CT PERFUSION|PERFUSION)(?:\s+(?:OF\s+THE\s+)?(?:HEAD|NECK|BRAIN))?\s*:", nc_text)
    if cut:
        rest = [nc_text[cut.start():]] + rest
        nc = [nc_text[:cut.start()].strip()] if nc_text[:cut.start()].strip() else []
        TXCOUNT["cta_split_inline_header_cut"] += 1
    sents = [x for x in split_sents(impression) if x.strip()]
    keep = [not VESSEL_NC.search(x) and not _NOT_HEAD.search(x) and not _CONTRAST_ONLY.search(x) for x in sents]
    # a sentence that only continues an angiographic one ("However, ...") goes with it
    keep = [k and not (i > 0 and not keep[i - 1] and _ORPHAN.match(sents[i])) for i, k in enumerate(keep)]
    nc_imp = " ".join(x for x, k in zip(sents, keep) if k)
    return "\n\n".join(nc), tidy_impression(nc_imp), "\n\n".join(rest)


_TREATMENT = re.compile(r"(?i)\bcoil(?:ing|ed|s)?\b|\bclip(?:ping|ped)?\b|thrombectom|\btPA\b|thromboly|\bstent|\bEVD\b|ventriculostom|"
                        r"external ventricular drain|catheter tip|craniectom|post-?procedur|post-?operative|post-?treatment|"
                        r"after (?:the )?(?:intervention|procedure|embolization)|embolization|endovascular")


_DEVICE_TX = re.compile(r"(?i)\bintubat\w*|endotracheal|\bET tube|\bETT\b|enteric tube|\bNG tube|nasogastric|orogastric|\bOG tube|"
                        r"\bventilat(?:ed|or)\b")
_DEVICE_CLAUSE = re.compile(r"(?i)[,;]?\s*(?:(?:which|that) (?:is|are|may be) )?(?:most |more )?(?:likely |possibly |probably )?(?:related|due|secondary|attributable)\s+to\s+"
                            r"(?:the\s+)?(?:patient'?s\s+)?(?:recent\s+)?(?:intubation|ETT|endotracheal|ventilation)\w*(?:\s+status)?[^.;]*")
TXCOUNT = collections.Counter()


def filter_sents(t: str, drop, counter: str) -> str:
    """Drop the sentences `drop` selects, and the sentences that only continue a dropped one."""
    xs = [x for x in split_sents(t) if x.strip()]
    flags = [bool(drop(x)) for x in xs]
    out = []
    for i, (x, f) in enumerate(zip(xs, flags)):
        if not f and i > 0 and flags[i - 1] and _ORPHAN.match(x) and not re.match(r"^\s*(?:no|there)\b", x, re.I):
            f = flags[i] = True
            TXCOUNT["orphan_piece_dropped"] += 1
        if f:
            TXCOUNT[counter] += 1
            continue
        out.append(x)
    return " ".join(out)


def drop_device_mentions(t: str) -> str:
    """Intubation and tubes are ED treatment unless the presentation shows them; reports do not reveal them."""
    out = []
    for x in split_sents(t or ""):
        y = _DEVICE_CLAUSE.sub("", x)
        if y != x:
            TXCOUNT["device_clause_cut"] += 1
            y = repair_fragment(y if y.rstrip().endswith((".", ";")) else y.rstrip() + ".", x)
            if not y:
                continue
            x = y
        out.append(x)
    return filter_sents(" ".join(out), _DEVICE_TX.search, "device_sentence_dropped")


def report_text(r: dict, later: bool = False) -> tuple[str, str, int, int]:
    f = re.search(FINDINGS, r["text"])
    findings = f.group(1).strip() if f else ""
    imp, n_items, n_drop = clean_impression(r["text"])
    def _para(p):
        xs = split_sents(_WS(p))
        ks = [clean_sentence(x) if (_RESULT_COMM.search(x) or _LATER.search(x) or _IMP_DROP.search(x) or _INFERENCE.search(x)
                                    or _IMP_CLAUSE.search(x) or _IMP_CLINICAL.search(x) or _DISEASE_RX.search(x)) else x for x in xs]
        return " ".join(k for k in orphan_rule(xs, ks) if k)
    findings = "\n\n".join(_para(p) for p in re.split(r"\n\s*\n", findings))
    findings = "\n\n".join(drop_value_blanks(p) for p in re.split(r"\n\s*\n", findings))
    imp = drop_value_blanks(imp)
    findings = "\n\n".join(drop_device_mentions(p) for p in re.split(r"\n\s*\n", findings))
    imp = drop_device_mentions(imp)
    if later:  # a study done after the work-up started may describe the treatment: those sentences go (with their orphans)
        keep = lambda t: filter_sents(t, _TREATMENT.search, "later_study_treatment_sentence_dropped")
        findings = "\n\n".join(keep(p) for p in re.split(r"\n\s*\n", findings))
        imp = tidy_impression(keep(imp))
    return findings, imp, n_items, n_drop


def first_rad(bundle: dict, t_ed, rx: str, lo: float, hi: float) -> list[dict]:
    rows = []
    for r in bundle["radiology"]:
        t = hours(r["charttime"], t_ed)
        if t is not None and lo <= t <= hi and re.search(rx, str(r["exam_name"]).upper()) and re.search(FINDINGS, r["text"]):
            rows.append({**r, "t_h": t})
    rows.sort(key=lambda r: r["t_h"])
    return rows


def ct_report(findings: str, impression: str, exam: str, contrast: bool, angio: str | None = None) -> dict:
    fs = [{"type": "report findings", "location": exam, "description": p} for p in paragraphs(findings)]
    out = {"findings": fs, "contrast_used": contrast, "additional_observations": [], "impression": impression,
           "recommended_actions": []}
    if angio is not None:
        out["angiography_findings"] = {exam: _WS(angio)}
    return out


# --- ECG from MIMIC-IV-ECG (decisions 1, 14) -----------------------------------------------------
def ecg_output(bundle: dict, t_ed, t_end) -> tuple[dict | None, dict]:
    rows = [r for r in bundle.get("ecg_machine", []) if hours(r["ecg_time"], t_ed) is not None
            and -1.0 <= hours(r["ecg_time"], t_ed) <= hours(t_end, t_ed) and r.get("report_0") not in (None, "")]
    if not rows:
        return None, {}
    r = sorted(rows, key=lambda x: x["ecg_time"])[0]
    lines = [str(r[f"report_{i}"]).strip() for i in range(18) if r.get(f"report_{i}") not in (None, "") and str(r.get(f"report_{i}")) != "nan"]
    # Machine boilerplate about the recording, not a statement about the ECG.
    lines = [x for x in lines if not re.search(r"(?i)age not entered|assumed to be|for purpose of ecg interpretation|"
                                               r"technically (?:limited|difficult)|unconfirmed|analysis error|no further analysis attempted", x)] or lines
    ok = lambda v: v is not None and str(v) != "nan" and float(v) < 29999 and float(v) not in (999.0, -999.0)
    rate = int(round(60000 / float(r["rr_interval"]))) if ok(r.get("rr_interval")) and float(r["rr_interval"]) > 0 else None
    if rate is None:
        return None, {"skipped": "no RR interval (decision 14: no rate, not served)"}
    iv = {}
    for name, a, b in (("PR", "p_onset", "qrs_onset"), ("QRS", "qrs_onset", "qrs_end"), ("QT", "qrs_onset", "t_end")):
        if ok(r.get(a)) and ok(r.get(b)) and float(r[b]) > float(r[a]):
            d_ = float(r[b]) - float(r[a])
            if (name == "PR" and not 80 <= d_ <= 400) or (name == "QRS" and not 40 <= d_ <= 250) or (name == "QT" and not 200 <= d_ <= 700):
                continue  # task 07: an implausible machine interval is not served
            iv[name] = f"{d_:.0f} ms"
    af = re.search(r"(?i)atrial (?:fibrillation|flutter)|\bafib\b", " ".join(lines)) is not None
    if af:
        iv.pop("PR", None)  # task 07: no PR interval or P axis on a tracing read as atrial fibrillation or flutter
    axis = ", ".join(f"{k} {int(float(r[c]))}" for k, c in (("P", "p_axis"), ("QRS", "qrs_axis"), ("T", "t_axis")) if ok(r.get(c)) and not (af and k == "P"))
    overall = [x for x in lines if re.search(r"(?i)\b(normal|abnormal|borderline|otherwise normal)\s+ecg\b", x)]
    out = {"rhythm": lines[0], "rate": rate, "intervals": iv, "axis": axis,
           "findings": [x for x in lines[1:] if x not in overall], "interpretation": " ".join(overall)}
    return out, {"origin": "table", "source": "MIMIC-IV-ECG machine_measurements (machine statements)",
                 "t_h": hours(r["ecg_time"], t_ed)}


# --- telemetry and respiratory function from ICU / ED records (decision 5) ----------------------
def telemetry_output(bundle: dict, t_ed, t_end) -> tuple[dict | None, dict]:
    ch = pd.DataFrame(bundle.get("icu_chart", []))
    rec = []
    if len(ch):
        ch["t"] = pd.to_datetime(ch.charttime)
        rr = ch[(ch.itemid == 220048) & (ch.t <= t_end)]
        rec += [(t, str(v)) for t, v in zip(rr.t, rr.value) if str(v) != "nan"]
    for v in bundle.get("ed_vitals", []):
        if v.get("rhythm") not in (None, "") and str(v.get("rhythm")) != "nan":
            rec.append((pd.Timestamp(v["charttime"]), str(v["rhythm"])))
    if not rec:
        return None, {}
    cov = rhythm_hours([t for t, _ in rec], t_end)
    if cov < 12:
        return None, {"skipped": f"rhythm records cover {cov:.1f} h (< 12 h)"}
    counts = collections.Counter(v for _, v in rec)
    hr = ch[(ch.itemid == 220045) & (ch.t <= t_end)].valuenum.dropna() if len(ch) else pd.Series(dtype=float)
    hr = hr[(hr >= 30) & (hr <= 250)]  # task 07: monitor artefacts below 30/min are not a heart rate  # task 06: implausible monitor values (0, artefacts) are not a heart rate
    ect = ch[(ch.itemid == 224650) & (ch.t <= t_end)] if len(ch) else pd.DataFrame()
    ect_counts = collections.Counter(str(v) for v in ect.value) if len(ect) else collections.Counter()
    non_sinus = {k: v for k, v in counts.items() if not re.search(r"(?i)sinus|\bSR\b|\bNSR\b", k)}
    out = {"duration_hours": int(round(cov)), "monitor_type": "telemetry",
           "rhythm_summary": "; ".join(f"{k}: {v} records" for k, v in counts.most_common()),
           "heart_rate_range": ({"min": int(hr.min()), "max": int(hr.max()), "average": int(round(hr.mean()))} if len(hr) else {}),
           "events": [{"type": "rhythm", "description": f"{k} recorded ({v} records)"} for k, v in non_sinus.items()]
                     + [{"type": "ectopy", "description": f"{k} ({v} records)"} for k, v in ect_counts.items() if k not in ("None", "nan")],
           "findings": [f"Telemetry over {cov:.0f} h."],
           "impression": ("Non-sinus rhythm recorded: " + ", ".join(non_sinus) if non_sinus else
                          "Only sinus rhythms recorded (" + ", ".join(counts) + "); no other rhythm recorded."),
           "recommended_actions": []}
    return out, {"origin": "table", "source": "icu/chartevents heart rhythm (220048) + ed/vitalsign rhythm", "covered_h": round(cov, 1)}


def resp_output(bundle: dict, t_ed) -> tuple[dict | None, dict]:
    ch = pd.DataFrame(bundle.get("icu_chart", []))
    if ch.empty:
        return None, {}
    ch["t"] = pd.to_datetime(ch.charttime)
    r = ch[ch.itemid.isin([224419, 220218, 224420]) & ch.valuenum.notna()].sort_values("t")
    if r.empty:
        return None, {}
    t1 = r.t.min()
    r = r[r.t <= t1 + pd.Timedelta(hours=24)]
    name = {224419: "Negative inspiratory force", 220218: "Vital capacity", 224420: "Vital capacity"}
    fs = [{"test": name[int(x.itemid)], "result": f"{x.valuenum:g} {'' if str(x.valueuom) == 'nan' else x.valueuom}".strip(),
           "time": f"+{(x.t - t1).total_seconds() / 3600:.0f} h"} for x in r.itertuples()]
    out = {"test_type": "respiratory_function", "findings": fs[:12],
           "quantitative_data": {n: f"first {g.valuenum.iloc[0]:g}, range {g.valuenum.min():g} to {g.valuenum.max():g}"
                                 for n, g in r.assign(n=r.itemid.map(name)).groupby("n")},
           "impression": "", "recommended_actions": []}
    return out, {"origin": "table", "source": "icu/chartevents NIF (224419) / vital capacity (220218, 224420), first 24 h of measurement",
                 "t_h": hours(t1, t_ed)}


# --- policy -------------------------------------------------------------------------------------
def condition_rules(out: Path, cond: str) -> tuple[list[str], list[str], list[str]]:
    f = out / ("06_strict.csv" if TAG[0] == "06" else "03_strict.csv")
    s = pd.read_csv(f).set_index("condition").loc[cond]
    from mimic_pilot_v3 import core_steps
    steps, panels = core_steps(cond)
    dropped = [] if pd.isna(s.panels_dropped) else str(s.panels_dropped).split(";")
    return steps, [p for p in panels if p not in dropped], dropped


def pattern_for(step: str, tmpl: dict, outputs: dict, followups: list, panels: list[str]) -> list[dict]:
    a0 = tmpl["alternatives"][0]
    if step == "labs":
        return [{"tool_name": "interpret_labs", "required_arguments": {"panels": panels}}]
    if step == "eeg":
        et = (outputs.get("eeg") or {}).get("eeg_type") or "continuous_icu"
        same = ["continuous_icu", "video"] if et in ("continuous_icu", "video") else [et]
        return [{"tool_name": "analyze_eeg", "required_arguments": {"eeg_type": x}} for x in same]
    if step == "mri_brain":
        args = {"contrast": bool(outputs.get("mri", {}).get("contrast_used"))}
        if "protocol" in a0["required_arguments"]:
            args["protocol"] = a0["required_arguments"]["protocol"]
        return [{"tool_name": "analyze_brain_mri", "required_arguments": args}]
    if step == "body:spine_MRI":
        return [{"tool_name": "order_body_imaging", "required_arguments": {"study": "spine_MRI", "contrast": bool(outputs.get("body_imaging", {}).get("contrast"))}}]
    if step == "cardiac_monitoring":
        return [{"tool_name": "order_cardiac_monitoring", "required_arguments": {"monitor_type": "telemetry"}}]
    if step == "echo":
        return [{"tool_name": "order_echocardiogram", "required_arguments": {"echo_type": "TTE"}}]
    if step == "csf":
        return [{"tool_name": "analyze_csf", "required_arguments": {}}]
    return [a0]


FACT_RULES = [  # (fact name, where to look, regex, conditions, kind, text)
    ("anticoagulant at home", "medications", r"warfarin|coumadin|apixaban|eliquis|rivaroxaban|xarelto|dabigatran|pradaxa|edoxaban|enoxaparin|lovenox",
     ["ISCH", "SAH"], "prohibited",
     "Do not give IV thrombolysis or proceed to invasive procedures before the anticoagulant, its last dose and its effect (coagulation tests) are established."),
    ("iodinated contrast allergy", "allergies", r"iodin|contrast|IV dye", ["ISCH", "SAH", "SE", "GBS", "MS"], "prohibited",
     "Do not give iodinated contrast without addressing the documented contrast allergy (premedication or an alternative study)."),
    ("antiseizure drug allergy", "allergies", r"tegretol|carbamazepine|zonegran|zonisamide|dilantin|phenytoin|lamictal|lamotrigine|keppra|levetiracetam|depakote|valpro|phenobarb|lacosamide|vimpat|topamax|topiramate|trileptal|oxcarbazepine",
     ["SE"], "prohibited", "Do not give the antiseizure medication documented as an allergy."),
    ("cardiac device", "history", r"pacemaker|\bICD\b|defibrillator|\bPPM\b", ["ISCH", "SAH", "SE", "GBS", "MS"], "avoided_mri",
     "MRI only after the documented cardiac device is confirmed MR-conditional."),
]


def draft_safety(cond: str, patient: dict, hpi: str) -> tuple[list[dict], list[str], list[dict]]:
    """Decision 18: avoided actions / prohibited recommendations only from documented facts, with pointers."""
    ch = patient["clinical_history"]
    fields = {"medications": " ; ".join(f"{m['drug']} {m['dose']}" for m in ch["medications"]),
              "allergies": " ; ".join(ch["allergies"]),
              "history": " ; ".join(ch["past_medical_history"]) + " ; " + hpi}
    avoided, prohibited, pointers = [], [], []
    for name, where, rx, conds, kind, text in FACT_RULES:
        if cond not in conds:
            continue
        m = re.search(rx, fields[where], re.I)
        if not m:
            continue
        ptr = {"fact": name, "field": where, "matched_term": m.group(0), "status": "draft for physician review"}
        if kind == "prohibited":
            prohibited.append(text)
            ptr["drafted"] = "assessment.prohibited_recommendations"
        else:
            avoided.append({"criterion_id": f"avoid-harm-{len(avoided) + 1}-analyze-brain-mri", "severity": "harm",
                            "alternatives": [{"tool_name": "analyze_brain_mri", "required_arguments": {}}],
                            "rationale": text + " (draft: documented device)", "citations": []})
            ptr["drafted"] = "avoided_actions"
        pointers.append(ptr)
    return avoided, prohibited, pointers


def diagnosis(cond: str, bundle: dict) -> tuple[dict, dict]:
    from apply_diagnosis_synonyms import entries_for, merge_overlay
    table = yaml.safe_load((ROOT / "agent-platform/config/policies/diagnosis_synonyms.yaml").read_text())
    table.pop("RETIRED", None)
    if OPTS.get("synonyms_overlay") and Path(OPTS["synonyms_overlay"]).exists():  # task 07, decision 43
        table = merge_overlay(table, yaml.safe_load(Path(OPTS["synonyms_overlay"]).read_text()) or {})
    p = bundle["diagnoses"][0]
    code, v10 = str(p["icd_code"]), int(p["icd_version"]) == 10
    dotted = f"{code[:3]}.{code[3:]}" if v10 and len(code) > 3 else code
    keys = ([dotted, code[:3] + "." + code[3:4]] if v10 else []) + [SYNONYM_CATEGORY[cond]]
    labels, codes = [], []
    for key in keys:
        for e in entries_for(key, CONDITION_ENUM[cond], table, bundle.get("case_id", "")):
            if e.get("cases") and bundle.get("case_id", "") not in e["cases"]:
                continue
            labels += [x for x in e.get("labels", []) if x not in labels]
            codes += [x for x in e.get("codes", []) if x not in codes]
    codes = ([dotted] if v10 else [ICD9_TO10[cond]]) + [c for c in codes if c != dotted]
    if not labels:
        labels = [p.get("long_title", "")]
    return ({"accepted": labels, "icd_codes": list(dict.fromkeys(codes)), "rejected": [], "required_components": []},
            {"principal_icd": f"ICD-{p['icd_version']} {code}", "principal_title": p.get("long_title", ""), "synonym_keys": keys})


from mimic_treat import AFFECTS as TREAT_AFFECTS, CLASSES as TREAT_CLASSES, blocked as treat_blocked  # noqa: E402

_TREAT = {}


def treatments_for(out: Path, hadm: int) -> pd.DataFrame:
    """Treatment rows of one admission (mimic_pilot_v4 labs4 -> 04_treatments.parquet)."""
    if "all" not in _TREAT:
        f = out / OPTS["treatments"]
        _TREAT["all"] = pd.read_parquet(f) if f.exists() else pd.DataFrame(columns=["hadm_id", "t", "source", "name", "classes"])
    t = _TREAT["all"]
    return t[t.hadm_id == hadm]


def case_flags(out: Path, cid: str) -> dict:
    """Decisions 25 / 26, decided by reading: 04_case_flags.csv (case_id, known_condition_in_history,
    known_condition_detail, dx_support, dx_support_basis)."""
    f = out / ("06_case_flags.csv" if TAG[0] == "06" and (out / "06_case_flags.csv").exists() else "04_case_flags.csv")
    if not f.exists():
        return {}
    d = pd.read_csv(f).fillna("")
    r = d[d.case_id == cid]
    if r.empty:
        return {}
    r = r.iloc[0].to_dict()
    r["known_condition_in_history"] = str(r.get("known_condition_in_history")).lower() in ("true", "1", "yes")
    return {k: v for k, v in r.items() if k != "case_id"}


def knowledge_levels(cases_dir: Path, cond: str) -> dict:
    """Decision 28: a knowledge tool takes the level the condition's NeuroBench cases give it, with the
    rule used for every other step: required in >= half the cases -> required; else required or
    recommended in >= half -> recommended; else present at all -> optional."""
    import collections as _c
    from mimic_pilot_cohort import step_key
    files = sorted(cases_dir.glob(f"{cond}-*.json"))
    lv = _c.defaultdict(_c.Counter)
    for f in files:
        seen = {}
        for c in json.loads(f.read_text())["ground_truth"]["action_criteria"]:
            k = step_key(c["alternatives"][0])
            if k in KNOWLEDGE:
                rank = {"required": 3, "recommended": 2, "optional": 1}.get(c["importance"], 0)
                seen[k] = max(seen.get(k, 0), rank)
        for k, r in seen.items():
            lv[k][r] += 1
    out = {}
    for k, c in lv.items():
        n = len(files)
        if c[3] >= n / 2:
            out[k] = "required"
        elif c[3] + c[2] >= n / 2:
            out[k] = "recommended"
        elif sum(c.values()):
            out[k] = "optional"
    return out


STEP_LABEL = {
    "ct_head": "Non-contrast head CT", "cta_head_neck": "CT angiography of the head and neck", "ecg": "12-lead ECG",
    "csf": "Lumbar puncture with CSF cell count, protein and glucose", "test:emg_ncs": "Nerve conduction studies and needle EMG",
    "test:respiratory_function": "Bedside respiratory function (vital capacity, negative inspiratory force)",
    "cardiac_monitoring": "Cardiac rhythm monitoring (telemetry)", "echo": "Transthoracic echocardiogram",
    "body:spine_MRI": "Spinal cord MRI", "knowledge:check_drug_interactions": "Check interactions of the planned treatment with the current medications",
    "knowledge:search_medical_literature": "Literature search",
}


def label_for(step: str, alts: list[dict], panels: list[str]) -> str:
    """A label that describes the criterion as transferred (its pattern), never the template patient."""
    if step == "labs":
        return "Blood tests: " + ", ".join(panels) if panels else "Blood tests"
    if step == "eeg":
        return "EEG (" + " or ".join(a["required_arguments"].get("eeg_type", "") for a in alts) + ")"
    if step == "mri_brain":
        a = alts[0]["required_arguments"]
        return "Brain MRI" + (" with contrast" if a.get("contrast") else " without contrast") + (f", {a['protocol']} protocol" if a.get("protocol") else "")
    return STEP_LABEL.get(step, step)


# --- one case -------------------------------------------------------------------------------------
def build_case3(cid: str, cond: str, out: Path, cases_dir: Path) -> tuple[dict, dict, list[str]]:
    bundle = json.loads((out / "02_source" / f"{cid}.json").read_text())
    draft = json.loads((out / "02_draft" / f"{cid}.json").read_text())
    man = json.loads((out / f"{TAG[0]}_manual" / f"{cid}.json").read_text())
    errors: list[str] = []
    counts = collections.Counter()
    DROPPED.clear()
    D24.clear()
    D27.clear()
    TXCOUNT.clear()
    note = bundle["discharge"][0]["text"]
    sec = draft["sections"]
    t_ed = anchor(bundle)
    adm = bundle["admission"][0]
    t_admit = ts(adm["admittime"])
    t24 = t_admit + pd.Timedelta(hours=24)
    t48 = t_admit + pd.Timedelta(hours=48)
    h24 = hours(t24, t_ed)

    # presentation
    hpi, removed, err = cut_hpi(sec.get("History of Present Illness", ""), man["hpi_removals"])
    counts["hpi_punctuation_repairs"] = sum(e.startswith("note: punctuation") for e in err)
    errors += [e for e in err if not e.startswith("note:")]
    if len(_WS(sec.get("History of Present Illness", ""))) < 50:
        errors.append("no HPI found in the note (section missing or header not parsed)")
    hpi, n = drop_ambiguous(hpi)
    counts["ambiguous_blank_sentences_dropped_hpi"] += n
    pat = bundle["patient"][0]
    age = int(pat["anchor_age"] + t_admit.year - pat["anchor_year"])
    if age > 89:
        errors.append("age above 89 (decision 11)")
    vit, vit_src = vitals(bundle)
    triage_cc = (bundle["triage"][0].get("chiefcomplaint") if bundle["triage"] else None) or ""
    cc, cc_src = str(triage_cc), "ed/triage"
    rw = man.get("chief_complaint_rewrite")
    if rw:
        cc, cc_src = rw["text"], f"rewritten from the kept HPI (decision {rw.get('decision', 7)}); triage original in the audit"
        for ph in rw.get("_verbatim", []):
            if not verbatim(ph, hpi):
                errors.append(f"chief complaint phrase not in the kept HPI: {ph[:30]!r}")
    exam_src = draft["admission_exam"] or note  # a de-identified exam header leaves the section empty: check against the note
    neuro, phys = dict(man["neurological_exam"]), dict(man.get("physical_exam", {}))
    for d in (neuro, phys):
        for k, v in list(d.items()):
            if not v:
                continue
            if not verbatim(v, exam_src):
                errors.append(f"exam field {k!r} is not verbatim from the admission exam")
            d[k], n = drop_ambiguous_fragments(v)
            counts["ambiguous_blank_fragments_dropped_exam"] += n
            d[k], n2 = (drop_blank_grids(d[k]) if OPTS["grid_mode"] == "drop" else GRID_CELLS(d[k]))
            counts["d27_exam_grid_fragments_dropped"] += n2
    ch = {}
    pmh = man.get("past_medical_history")
    if pmh is None:
        lines: list[str] = []
        for x in sec.get("Past Medical History", "").splitlines():
            x = _WS(x)
            if not x.strip(" -*•") or x == "___":
                continue
            if lines and (re.match(r"^[a-z(]", x) or re.search(r"(?:\bof|\band|\bwith|\bs/p|;|,)$", lines[-1])):
                lines[-1] += " " + x
            else:
                lines.append(x)
        pmh = [x.lstrip("-*• ").strip() for x in lines]
    for item in pmh:
        if not verbatim(item, sec.get("Past Medical History", "")) and not verbatim(item, note.split("Social History:")[0]):  # task 06: repeated PMH headings
            errors.append(f"PMH item not verbatim: {item[:40]!r}")
    kept_pmh = []
    for item in pmh:
        x, n = drop_ambiguous(item)
        counts["ambiguous_blank_dropped_pmh"] += n
        if x and _NORM(x) not in ("", "___"):
            kept_pmh.append(x)
    ch["past_medical_history"] = kept_pmh
    meds = man.get("medications")
    meds_src = "note: Medications on Admission (parsed)"
    if meds is None:
        meds = parse_medications(sec.get("Medications on Admission", ""))
    meds = [m for m in meds if not re.match(r"(?i)^(the preadmission|___)", m["drug"])]
    if not meds and bundle["ed_medrecon"]:
        meds = [{"drug": m["name"], "dose": "", "frequency": "", "indication": ""} for m in bundle["ed_medrecon"]]
        meds_src = "ed/medrecon (names only)"
    if not meds:
        meds_src = "none recorded"
    ch["medications"] = meds
    allergies = man.get("allergies")
    if allergies is None:
        raw = re.split(r"\n\s*\n|Attending:", sec.get("Allergies", ""))[0]
        if re.match(r"(?i)\s*(?:no known allergies|patient recorded as having no known allergies)", raw):
            allergies = [_WS(raw)]
        else:
            allergies = [_WS(x) for x in re.split(r"\s/\s|,", raw) if _WS(x)]
    al = []
    for x in allergies:
        y, n = drop_ambiguous(x)
        counts["ambiguous_blank_dropped_allergies"] += n
        if y:
            al.append(y)
    ch["allergies"] = al
    fam = man.get("family_history")
    if fam is None:
        fh = re.sub(r"(?<![.:;])\n(?=\s*[a-z_(])|(?<=\bwith)\n|(?<=\bof)\n|(?<=\band)\n", " ", sec.get("Family History", ""))  # join line wraps
        fam = [_WS(x) for x in re.split(r"\n|(?<=\.)\s+", fh) if _WS(x) and _WS(x).lower() not in ("unknown", "___", "noncontributory", "non-contributory")]
    fm = []
    for x in fam:
        y, n = drop_ambiguous(x)
        counts["ambiguous_blank_dropped_family"] += n
        if y:
            fm.append(y)
    ch["family_history"] = fm
    ch["social_history"] = man.get("social_history", {})
    size = body_size(bundle, t_admit)
    patient = {"patient_id": cid,
               "demographics": {"age": age, "sex": "female" if pat["gender"] == "F" else "male", "handedness": man.get("handedness", ""),
                                "ethnicity": str(adm.get("race") or "").title(), **size},
               "clinical_history": ch, "neurological_exam": neuro, "physical_exam": phys, "vitals": vit,
               "chief_complaint": cc, "history_present_illness": hpi}

    # tool outputs
    served: dict[str, dict] = {}
    outputs: dict = {}
    followups: list[dict] = []
    first = lab_rows(bundle, t_ed - pd.Timedelta(hours=1), t24)
    if len(first):
        n0 = len(first)
        first = first[~(first.valuenum.isna() & first.value.astype(str).str.fullmatch(r"\s*_{3}\s*", na=False))]
        counts["lab_placeholder_rows_dropped"] += n0 - len(first)
        vent = first.label.str.contains(r"(?i)^intubated$|ventilat|\bPEEP\b|tidal volume|^O2 Flow$|required O2|^Rates$|^Vent|^Oxygen$", regex=True, na=False)
        counts["lab_ventilator_rows_dropped"] += int(vent.sum())
        first = first[~vent]
        AED = {"Phenytoin": r"phenyto|dilantin", "Free Phenytoin": r"phenyto|dilantin", "Valproic Acid": r"valpro|depak",
               "Levetiracetam": r"levetir|keppra", "Phenobarbital": r"phenobarb", "Carbamazepine": r"carbamaz|tegretol",
               "Lacosamide": r"lacosam|vimpat", "Lamotrigine": r"lamotri|lamictal"}
        doses = [(pd.Timestamp(m["charttime"]), str(m["name"])) for m in bundle.get("ed_pyxis", []) if m.get("charttime")]
        home = " ".join(f"{m['drug']}" for m in (man.get("medications") or parse_medications(sec.get("Medications on Admission", ""))))
        drop = []
        for i, row in first.iterrows():
            rx = AED.get(row.label)
            # A level after an ED dose, or of a drug the patient does not take at home, shows the ED load.
            if rx and (any(re.search(rx, nm, re.I) and t <= row.t for t, nm in doses) or not re.search(rx, home, re.I)):
                drop.append(i)
        counts["aed_levels_after_ed_dose_dropped"] += len(drop)
        first = first.drop(index=drop)
        # Decision 23: a value drawn after a treatment that changes that analyte (ED pyxis, emar,
        # prescriptions where no emar, ICU inputs / ventilation) is not served.
        tr = treatments_for(out, bundle["hadm_id"])
        tt = {k: tr[tr.classes.str.contains(k, na=False)].t.min() for k in TREAT_CLASSES} if len(tr) else {}
        # Intubated before arrival (EMS) or on arrival: the presentation says so; every gas is on the ventilator.
        pres_txt = hpi + " " + " ".join(str(v) for v in list(neuro.values()) + list(phys.values()) if v) + " " + " ".join(man.get("exam_devices_kept", []))
        if re.search(r"(?i)\bintubat|\bETT\b|endotracheal|on the vent|ventilator", pres_txt):
            tt["ventilation"] = min([x for x in (tt.get("ventilation"), t_ed - pd.Timedelta(hours=1)) if pd.notna(x)])
            counts["ventilation_known_from_presentation"] += 1
        aed_doses = list(zip(tr[tr.classes.str.contains("antiseizure", na=False)].t, tr[tr.classes.str.contains("antiseizure", na=False)].name)) if len(tr) else []
        intub_spec = set()
        if "specimen_id" in first:
            allb = pd.DataFrame(bundle["labs"])
            if len(allb) and "specimen_id" in allb:
                iv = allb[allb.label.astype(str).str.fullmatch(r"(?i)intubated|ventilator", na=False)
                          & allb.value.astype(str).str.contains(r"(?i)intubat|control|assist|imv|vent", na=False)]
                intub_spec = set(iv.specimen_id)
        drop23 = []
        for i, row in first.iterrows():
            k = treat_blocked(row.label, row.t, tt, aed_doses)
            if not k and row.label in TREAT_AFFECTS["ventilation"] and row.get("specimen_id") in intub_spec:
                k = "ventilation"
            if k:
                drop23.append(i)
                counts[f"lab_d23_{k}_dropped"] += 1
        first = first.drop(index=drop23)
        t_med = tr[tr.source == "ed_pyxis"].t.min() if len(tr) else pd.NaT
        counts["labs_served_values"] += len(first)
        counts["labs_served_after_first_ed_med"] += int((first.t > t_med).sum()) if pd.notna(t_med) else 0
    labs, _, lab_serving = labs_output(first, t_ed)
    if labs:
        outputs["labs"] = labs
        served["labs"] = {"origin": "table", "source": "hosp/labevents (first value per item, ED arrival - 1 h to admission + 24 h)", **lab_serving}
    al_ = pd.DataFrame(bundle["labs"])
    if len(al_):
        al_["t"] = pd.to_datetime(al_.charttime)
        c = al_[(al_.fluid == "Cerebrospinal Fluid") & ~(al_.hadm_id.notna() & (al_.hadm_id != bundle["hadm_id"]))
                & (al_.value.notna() | al_.valuenum.notna())]
        if len(c):
            c = c[c.t <= c.t.min() + pd.Timedelta(hours=1)].sort_values("t").drop_duplicates("itemid")
            blank = c.valuenum.isna() & c.value.astype(str).str.contains(r"_{3}", na=False) & ~c.value.astype(str).str.contains(r"\d", na=False)
            counts["csf_blank_values_dropped"] += int(blank.sum())  # decision 27
            counts["csf_masked_text_served_from_valuenum"] += int((c.valuenum.notna() & c.value.astype(str).str.fullmatch(r"\s*_{3}\s*", na=False)).sum())
            c = c[~blank]
            labs_present = " ; ".join(c.label.astype(str))
            core_ok = all(re.search(rx, labs_present, re.I) for rx in (r"WBC|Total Nucleated|White Blood|Polys|Lymphs|RBC", r"Protein", r"Glucose"))
            if len(c):
                _, csf, _ = labs_output(c, t_ed)
                outputs["csf"] = csf
                served["csf"] = {"origin": "table", "source": "hosp/labevents CSF (first sample)", "t_h": hours(c.t.min(), t_ed),
                                 "core_elements_complete": core_ok}
            if not core_ok:
                counts["csf_core_element_missing"] += 1
    for d in man.get("radiology_drop_sentences", []):
        for r in bundle["radiology"]:
            r["text"], k = drop_sentences(r["text"], [d["sentence"]])
            counts["radiology_reader_drops"] += k
    nc = first_rad(bundle, t_ed, NCCT_EXAM, -1.0, h24)
    cta = first_rad(bundle, t_ed, CTA_EXAM, -1.0, h24)
    cta_reports = [r for r in cta if r["t_h"] - cta[0]["t_h"] <= 3.0] if cta else []
    seen, uniq = set(), []
    for r in cta_reports:
        if _WS(r["text"]) not in seen:
            seen.add(_WS(r["text"]))
            uniq.append(r)
        else:
            uniq[-1] = {**uniq[-1], "exam_name": uniq[-1]["exam_name"] + " + " + r["exam_name"]}
    cta_reports = uniq
    cta_texts = {_WS(r["text"]) for r in cta}
    nc = [r for r in nc if _WS(r["text"]) not in cta_texts and not re.search(r"(?im)^\s*(?:CTA|CT ANGIO)[^\n:]{0,40}:", r["text"])]
    use_sep = bool(nc) and (not cta or nc[0]["t_h"] <= cta[0]["t_h"] + 0.5 or cond not in ("ISCH", "SAH"))
    if use_sep:
        f_, imp, ni, nd = report_text(nc[0])
        counts["impression_sentences"] += ni
        counts["impression_sentences_dropped"] += nd
        f_, k = drop_ambiguous(f_)
        imp, k2 = drop_ambiguous(imp)
        counts["ambiguous_blank_sentences_dropped_reports"] += k + k2
        f_, imp = no_other_study(f_, "ct"), no_other_study(imp, "ct")
        outputs["ct"] = ct_report(f_, imp, nc[0]["exam_name"], False)
        served["ct"] = {"origin": "table", "source": "note/radiology (findings + cleaned impression)", "exam": nc[0]["exam_name"], "t_h": nc[0]["t_h"]}
    if cta_reports:
        fs, imps = [], []
        for r in cta_reports:
            f_, imp, ni, nd = report_text(r)
            counts["impression_sentences"] += ni
            counts["impression_sentences_dropped"] += nd
            fs.append(f_)
            imps.append(imp)
        full_f, full_i = "\n\n".join(fs), " ".join(imps)
        cta_f = full_f
        _nc_lead = re.compile(r"(?im)^\s*(?:FINDINGS?\s*:\s*)?(?:The\s+)?(?:pre-?\s?contrast|non-?\s?contrast|noncontrast|unenhanced|non-?enhanced)\s+"
                              r"(?:images?|scan|study|portion|series|(?:head\s+)?CT)\b")
        has_nc = NONCONTRAST_IN_CTA.search("\n".join(r["text"] for r in cta_reports)) or _nc_lead.search(full_f)
        if use_sep and has_nc:  # task 07: a separate plain CT answers that order; the CTA answer still leaves out the non-contrast part
            ncf, nci, rest = split_cta(full_f, full_i)
            if ncf.strip():
                cta_f = rest
                counts["cta_nc_part_removed_separate_ct"] += 1
        if not use_sep and has_nc:
            ncf, nci, rest = split_cta(full_f, full_i)
            if ncf.strip():
                ncf, k = drop_ambiguous(ncf)
                ncf, nci = no_other_study(ncf, "ct"), no_other_study(nci, "ct")
                outputs["ct"] = ct_report(ncf, nci, "CT HEAD WITHOUT CONTRAST", False)
                served["ct"] = {"origin": "table", "source": "note/radiology, explicit non-contrast part of the CTA report (decision 2)",
                                "exam": cta_reports[0]["exam_name"], "t_h": cta_reports[0]["t_h"]}
                cta_f = rest
                counts["ct_from_cta_split"] += 1
        if has_nc:
            keep_s = [x for x in split_sents(full_i) if x.strip() and (VESSEL.search(x) or _NOT_HEAD.search(x))]
            TXCOUNT["cta_impression_nc_sentences_removed"] += len([x for x in split_sents(full_i) if x.strip()]) - len(keep_s)
            full_i = tidy_impression(" ".join(keep_s))
        cta_f, k = drop_ambiguous(cta_f)
        full_i, k2 = drop_ambiguous(full_i)
        counts["ambiguous_blank_sentences_dropped_reports"] += k + k2
        exam = " + ".join(r["exam_name"] for r in cta_reports)
        followups.append({"trigger_action": "request_ct_angiography", "tool_name": "order_ct_scan",
                          "output": ct_report(cta_f, full_i, exam, True, angio=cta_f)})
        served["followup:request_ct_angiography"] = {"origin": "table", "source": "note/radiology (findings + cleaned impression)",
                                                     "exam": exam, "t_h": cta_reports[0]["t_h"]}
    mri = first_rad(bundle, t_ed, MRI_EXAM, -1.0, draft["t_disch_h"])
    if mri:
        f_, imp, ni, nd = report_text(mri[0], later=True)
        counts["impression_sentences"] += ni
        counts["impression_sentences_dropped"] += nd
        paras, in_mra = [], False
        for p in paragraphs(f_):
            in_mra = bool(re.match(r"(?i)(?:(?:BRAIN|HEAD|NECK)\s+)?MR[AV]\b|MR (?:angiogra|venogra)", p)) or (in_mra and not re.match(r"(?i)MR(I)? (?:OF THE )?(head|brain|orbits?)\b|(?:BRAIN|ORBITS?) MRI\b", p))
            if not in_mra:
                paras.append(drop_ambiguous(p)[0])
        has_mrv = bool(re.search(r"(?i)\bMRV\b|MR VENO", mri[0]["text"]))
        imp = tidy_impression(" ".join(s for s in split_sents(imp) if not re.search(r"(?i)\bMR[AV]\b|angiogra|venogra", s)
                                       and not (has_mrv and re.search(r"(?i)(?:dural|venous|sagittal|transverse|sigmoid|straight)\s+sinus|sinus thrombosis", s))))
        if re.search(r"(?i)\bMRA\b|MR ANGIO|\bMRV\b|NECK MRA|HEAD MRA", mri[0]["text"]):
            vt = lambda x: (VESSEL.search(x) or _NOT_HEAD.search(x)) and not re.search(r"(?i)flow voids?|venous sinus|dural sinus", x)
            n0 = len(paras)
            paras = [filter_sents(p, vt, "mri_mra_sentence_dropped") for p in paras]
            imp = tidy_impression(filter_sents(imp, vt, "mri_mra_sentence_dropped"))
            TXCOUNT["mri_mra_content_removed"] += 1
        outputs["mri"] = {"contrast_used": bool(re.search(r"W ?& ?W/O|W/ CONTRAST|WITH CONTRAST", mri[0]["exam_name"].upper())),
                          "findings": [], "additional_observations": [p for p in paras if p], "impression": drop_ambiguous(imp)[0],
                          "recommended_actions": []}
        served["mri"] = {"origin": "table", "source": "note/radiology (findings + cleaned impression)", "exam": mri[0]["exam_name"], "t_h": mri[0]["t_h"]}
    sp = first_rad(bundle, t_ed, SPINE_MRI_EXAM, -1.0, draft["t_disch_h"])
    if sp:
        same = [r for r in sp if r["t_h"] - sp[0]["t_h"] <= 3.0]
        names = list(dict.fromkeys(r["exam_name"] for r in same))
        sp = [{**sp[0], "exam_name": " + ".join(names)}]
        # task 07: one report holding several spine levels ("MRI OF THE CERVICAL SPINE: ... MRI OF THE THORACIC SPINE: FINDINGS ...")
        secs = re.split(r"(?im)^\s*(?=(?:MRI?|MR)\s+OF\s+THE\s+[A-Z ]*SPINE\s*:)", sp[0]["text"])
        if len([x for x in secs if re.match(r"(?i)\s*(?:MRI?|MR)\s+OF\s+THE\s+[A-Z ]*SPINE\s*:", x)]) > 1:
            fs_, is_ = [], []
            for sec_ in secs:
                if not re.search(FINDINGS, sec_) and not IMPRESSION.search(sec_):
                    continue
                if not re.search(r"(?i)\bFINDINGS?\s*:", sec_):  # a level section without its own FINDINGS label
                    sec_ = re.sub(r"(?i)^(\s*(?:MRI?|MR)\s+OF\s+THE\s+[A-Z ]*SPINE\s*:)", r"\1\nFINDINGS:", sec_, count=1)
                f1, i1, ni, nd = report_text({**sp[0], "text": sec_}, later=True)
                head = re.match(r"\s*((?:MRI?|MR)\s+OF\s+THE\s+[A-Z ]*SPINE)\s*:", sec_)
                lab = (head.group(1).strip() + ": ") if head else ""
                fs_.append(lab + f1 if f1 else "")
                is_.append(lab + i1 if i1 else "")
                counts["impression_sentences"] += ni
                counts["impression_sentences_dropped"] += nd
            f_, imp = "\n\n".join(x for x in fs_ if x), " ".join(x for x in is_ if x)
            TXCOUNT["spine_report_sections_split"] += 1
        else:
            f_, imp, ni, nd = report_text(sp[0], later=True)
            counts["impression_sentences"] += ni
            counts["impression_sentences_dropped"] += nd
        outputs["body_imaging"] = {"region": "spine", "modality": "MRI",
                                   "contrast": bool(re.search(r"W ?& ?W/O|W/ CONTRAST|WITH CONTRAST", sp[0]["exam_name"].upper())),
                                   "findings": [{"finding": drop_ambiguous(p)[0], "location": sp[0]["exam_name"]} for p in paragraphs(f_)],
                                   "impression": drop_ambiguous(imp)[0], "recommended_actions": []}
        served["body_imaging"] = {"origin": "table", "source": "note/radiology (findings + cleaned impression)", "exam": sp[0]["exam_name"], "t_h": sp[0]["t_h"]}
    e, es = ecg_output(bundle, t_ed, t24)
    if e:
        outputs["ecg"] = e
        served["ecg"] = es
    elif es:
        counts["ecg_skipped_no_rate"] += 1
    tele, tsrc = telemetry_output(bundle, t_ed, t48)
    if tele:
        outputs["cardiac_monitoring"] = tele
        served["cardiac_monitoring"] = tsrc
    resp, rsrc = resp_output(bundle, t_ed)
    resp_out = resp
    # note-extracted studies (reader); a table answer, when present, wins for telemetry / respiration
    for key, schema_key in (("eeg", "eeg"), ("echo", "echo"), ("telemetry", "cardiac_monitoring"), ("emg", "specialized_test"),
                            ("respiratory_function", "resp")):
        x = man.get(key)
        if not x:
            continue
        x = dict(x)
        src = x.pop("_verbatim_source", None)
        for phrase in x.pop("_verbatim", []):
            if not verbatim(phrase, note):
                errors.append(f"{key}: phrase not verbatim in the note: {phrase[:40]!r}")
        if schema_key == "resp":
            x = walk_strings(walk_strings(walk_strings(x, strip_disease_text), drop_value_blanks), strip_provenance)
            if resp_out is None:
                resp_out, rsrc = x, {"origin": "note_extracted", "source": src or "discharge note"}
            continue
        x = walk_strings(walk_strings(walk_strings(x, strip_disease_text), drop_value_blanks), strip_provenance)
        if schema_key == "eeg" and OPTS["eeg_strip_treatment"]:
            x = walk_strings(x, strip_eeg_treatment)
        for lk in ("limitations",):
            if isinstance(x.get(lk), str) and re.search(r"(?i)\bnote\b|hospital[- ]course|discharge|narrative|extracted|pertinent results|summary", x[lk]):
                x[lk] = ""
                counts["provenance_text_removed"] += 1
        if schema_key in outputs:
            continue
        outputs[schema_key] = x
        served[schema_key] = {"origin": "note_extracted", "source": src or "discharge note"}
    if resp_out is not None:
        followups.append({"trigger_action": "request_respiratory_monitoring", "tool_name": "order_specialized_test", "output": resp_out})
        served["followup:request_respiratory_monitoring"] = rsrc

    # policy
    steps, panels, dropped = condition_rules(out, cond)
    have = {"ct_head": "ct" in outputs, "cta_head_neck": any(f["trigger_action"] == "request_ct_angiography" for f in followups),
            "labs": "labs" in outputs, "ecg": "ecg" in outputs, "eeg": "eeg" in outputs,
            "csf": "csf" in outputs and served.get("csf", {}).get("core_elements_complete", False),
            "test:emg_ncs": outputs.get("specialized_test", {}).get("test_type") == "emg_ncs",
            "test:respiratory_function": any(f["trigger_action"] == "request_respiratory_monitoring" for f in followups),
            "cardiac_monitoring": "cardiac_monitoring" in outputs, "mri_brain": "mri" in outputs,
            "body:spine_MRI": "body_imaging" in outputs, "echo": "echo" in outputs,
            "knowledge:check_drug_interactions": True, "knowledge:search_medical_literature": True,
            # task 06: steps of the new conditions (served by mimic_case_build6 from the manual file / tables)
            "perform_clinical_assessment": bool(man.get("clinical_assessment")),
            "obtain_tissue_diagnosis": bool(man.get("tissue_diagnosis")),
            "micro:ascitic_fluid": any(str(m.get("spec_type_desc", "")).upper().startswith("PERITONEAL FLUID") for m in bundle.get("micro", [])),
            "micro:blood_culture": any(str(m.get("spec_type_desc", "")).upper().startswith("BLOOD CULTURE") for m in bundle.get("micro", []))}
    if labs:
        missing = [p for p in panels if p not in labs["panels"]]
        if missing:
            have["labs"] = False
            errors.append(f"required lab panels not resulted: {missing}")
    for s in steps:
        if not have.get(s, False):
            errors.append(f"core step {s} has no served result")
    criteria, prov = [], {}
    klevel = knowledge_levels(cases_dir, cond)  # decision 28: the template's own level
    steps = [s for s in steps if not s.startswith("knowledge") or klevel.get(s) == "required"]
    order = steps + [s for s in RECOMMENDED.get(cond, []) if s not in steps and have.get(s)]
    order += [k for k, v in klevel.items() if v in ("recommended", "optional") and k not in order]
    level = {**{s: "required" for s in steps}, **{s: "recommended" for s in RECOMMENDED.get(cond, [])},
             **{k: v for k, v in klevel.items() if k not in steps}}
    for i, step in enumerate(order, start=1):
        tmpl, n = template_criterion(cases_dir, cond, step)
        alts = pattern_for(step, tmpl, outputs, followups, panels)
        cid_ = f"action-{i}-{alts[0]['tool_name'].replace('_', '-')}"
        lab_ = label_for(step, alts, panels)
        criteria.append({"criterion_id": cid_, "label": lab_, "importance": level.get(step, "recommended"),
                         "alternatives": alts, "expected_evidence": "",
                         "rationale": f"Transferred from the NeuroBench {cond} policy (step required, recommended or optional at the level "
                                      f"of the condition's cases); the template wording is not used because it describes a synthetic patient.",
                         "citations": tmpl.get("citations", [])})
        prov[cid_] = {"step": step, "template_pattern_cases": n}
    ids = {prov[c["criterion_id"]]["step"]: c["criterion_id"] for c in criteria}
    seq = []
    if "ct_head" in ids and "cta_head_neck" in ids:
        seq.append({"before_criterion_id": ids["ct_head"], "after_criterion_id": ids["cta_head_neck"],
                    "reason": "The non-contrast CT precedes the CT angiogram (transferred from the NeuroBench policy).",
                    "citations": [], "severity": "soft"})
    avoided, prohibited, pointers = draft_safety(cond, patient, hpi)
    if "mri" in outputs:  # the record shows the MRI was done, so the device permitted it: no avoided MRI is drafted
        avoided = [x for x in avoided if "analyze-brain-mri" not in x["criterion_id"]]
        pointers = [x for x in pointers if x.get("drafted") != "avoided_actions"]
    flags4 = case_flags(out, cid)
    for k, v in D24.items():
        counts[f"d24_{k}"] += v
    for k, v in D27.items():
        counts[f"d27_value_blank_{k}"] += v
    for k, v in TXCOUNT.items():
        counts[f"r3_{k}"] += v
    dx, dx_info = diagnosis(cond, bundle)
    gt = {"review_status": "draft", "diagnosis": dx, "differential": [], "action_criteria": criteria, "avoided_actions": avoided,
          "sequence_constraints": seq,
          "stop_rule": {"required_before_assessment": [c["criterion_id"] for c in criteria if c["importance"] == "required"],
                        "max_additional_actions": 1},
          "assessment": {"required_recommendations": [], "prohibited_recommendations": prohibited},
          "key_clinical_evidence": [], "red_herrings": []}
    case = {"schema_version": "2.0", "case_id": cid, "domain": "neurology", "provenance": "record",
            "condition": CONDITION_ENUM[cond], "difficulty": "moderate", "encounter_type": "emergency",
            "patient": patient, "initial_tool_outputs": outputs, "followup_outputs": followups, "ground_truth": gt,
            "metadata": {"source": "MIMIC-IV 3.1 + ED 2.2 + Note 2.2 + ECG 1.0 (credentialed; id map in 03_selection.csv)",
                         "builder": "mimic_case_build3.py (task 03)", "served": served,
                         "presentation_sources": {"chief_complaint": cc_src, "vitals": vit_src, "medications": meds_src,
                                                  "history_present_illness": "note HPI, cut by the reader (03_hpi_audit)",
                                                  "exam": "note admission exam, fields by the reader (verbatim)"},
                         "policy": {"status": "draft", "transferred_from": f"NeuroBench {cond} cases", "criteria": prov,
                                    "lab_panels_dropped_rule_3": dropped},
                         "diagnosis_source": {**dx_info, "discharge_diagnosis": _WS(sec.get("Discharge Diagnosis", "")),
                                              "record_support": man.get("dx_support", {})},
                         "safety_drafts": pointers,
                         "reference_trajectory": trajectory(bundle, t_ed),
                         "timing_hours_from_ed_arrival": {"admission": draft["t_admit_h"], "discharge": draft["t_disch_h"], "window_24h_end": h24},
                         "known_condition_in_history": flags4.get("known_condition_in_history", False),
                         "known_condition_detail": flags4.get("known_condition_detail", ""),
                         "dx_support": flags4.get("dx_support", ""),
                         "dx_support_basis": flags4.get("dx_support_basis", ""),
                         "build_counts": dict(counts), "difficulty_note": "not graded for recorded cases; 'moderate' is a placeholder"}}
    audit = {"case_id": cid, "hpi_original": _WS(sec.get("History of Present Illness", "")), "hpi_kept": hpi, "removed": removed,
             "removed_counts": dict(collections.Counter(r["class"] for r in removed)),
             "chief_complaint_triage_original": str(triage_cc), "chief_complaint_shown": cc,
             "exam_cuts": man.get("exam_cuts", []), "exam_devices_kept": man.get("exam_devices_kept", []),
             "exam_notes": man.get("exam_notes", []), "other_edits": man.get("other_edits", []),
             "safety_pointers": pointers, "dx_support": man.get("dx_support", {}), "flags_04": flags4, "build_counts": dict(counts),
             "ambiguous_blank_dropped": list(DROPPED)}
    return case, audit, errors


def perfect_agent3(cases_dir: Path, cid: str) -> tuple[list[str], list[str], list[str]]:
    """The repository's perfect-agent check; a library answer to a knowledge tool is legitimate (decision 17)."""
    import perfect_agent as pa
    pa.CASES = cases_dir
    errs, warns = pa.check(cid)
    knowledge = ("check_drug_interactions", "search_medical_literature")
    accepted = [e for e in errs if any(k in e for k in knowledge) and "benchmark library" in e]
    rest = [e for e in errs if e not in accepted]
    # The library answer leaves those criteria unscored as fallback; the score components that only
    # fail because of it are accepted too.
    if accepted:
        rest = [e for e in rest if not e.startswith("perfect agent scores")]
    return rest, warns, accepted


def build_all3(a) -> None:
    from neuroagent_schemas import NeuroBenchCase
    from mimic_case_review import review_md
    out = Path(a.out)
    sel = pd.read_csv(out / a.selection)
    sel = sel[sel.case_id.notna() & (sel.case_id != "")]
    if a.cases_only:
        sel = sel[sel.case_id.isin(a.cases_only)]
    TAG[0] = getattr(a, "tag", "03")
    T = TAG[0]
    cdir = out / f"{T}_cases"
    for d in (f"{T}_cases", f"{T}_hpi_audit", f"{T}_review"):
        (out / d).mkdir(exist_ok=True)
    path = out / f"{T}_build_checks.json"
    checks = json.loads(path.read_text()) if path.exists() else {}
    for r in sel.itertuples():
        if not (out / f"{T}_manual" / f"{r.case_id}.json").exists():
            print(f"{r.case_id}: no manual file yet", file=sys.stderr)
            continue
        case, audit, errors = build_case3(r.case_id, r.condition, out, Path(a.cases))
        try:
            NeuroBenchCase.model_validate(case)
            valid = "ok"
        except Exception as exc:
            valid = f"INVALID: {exc}"
        (cdir / f"{r.case_id}.json").write_text(json.dumps(case, indent=1, default=str))
        (out / f"{T}_hpi_audit" / f"{r.case_id}.json").write_text(json.dumps(audit, indent=1))
        pa_err, pa_warn, pa_acc = perfect_agent3(cdir, r.case_id) if valid == "ok" else (["not run: invalid"], [], [])
        checks[r.case_id] = {"condition": r.condition, "schema": valid, "build_errors": errors, "perfect_agent_errors": pa_err,
                             "perfect_agent_warnings": pa_warn, "perfect_agent_knowledge_library_accepted": pa_acc}
        (out / f"{T}_review" / f"{r.case_id}.md").write_text(review_md(case, audit))
        print(f"{r.case_id}: schema {valid[:50]}; build errors {len(errors)}; perfect agent {'ok' if not pa_err else 'FAIL ' + str(len(pa_err))}",
              file=sys.stderr)
        for e in errors + pa_err:
            print(f"    {e}", file=sys.stderr)
    path.write_text(json.dumps(checks, indent=1))
