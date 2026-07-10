"""Filter MedCaseReasoning for neurology cases and assign to NeuroBench conditions.

Downloads from HuggingFace, filters by neurology keywords per condition,
ranks by case quality, assigns difficulty levels, and outputs seed JSONs.

Usage:
    uv run python dataset-generation/scripts/filter_medcasereasoning.py \
        --output dataset-generation/seeds \
        --target-per-condition 30 \
        --exclude-pmcids data/neurobench/cases
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
from collections import defaultdict
from pathlib import Path

from datasets import load_dataset

logger = logging.getLogger(__name__)

# ── Condition keyword filters ──────────────────────────────────────────────
# Each condition maps to (diagnosis_keywords, presentation_keywords).
# diagnosis_keywords: matched against final_diagnosis (high signal)
# presentation_keywords: matched against case_prompt (broader, used as tiebreaker)
# All matching is case-insensitive.

CONDITION_FILTERS: dict[str, dict] = {
    "ischemic_stroke": {
        "abbreviation": "ISCH-STR",
        "diagnosis_keywords": [
            r"\bischemic\s+stroke\b", r"\bcerebral\s+infarct", r"\bacute\s+stroke\b",
            r"\bmca\s+(territory\s+)?infarct", r"\blacunar\s+(infarct|stroke)\b",
            r"\bcardioembolic\s+stroke\b", r"\bcryptogenic\s+stroke\b",
            r"\bbasilar\s+(artery\s+)?occlusion\b", r"\bvertebral\s+artery\s+dissection\b",
            r"\bcarotid\s+(artery\s+)?dissection\b", r"\bwallenberg\b",
            r"\blateral\s+medullary\b", r"\bantiphospholipid.*stroke\b",
            r"\bcerebral\s+venous\s+thromb", r"\bpercheron\s+infarct",
            r"\bcerebrovascular\b", r"\btransient\s+ischemic\s+attack\b",
            r"\bintracranial\s+(stenosis|occlusion)\b",
            r"\bposterior\s+reversible\s+encephalopathy\b",
            r"\bcerebral\s+amyloid\s+angiopathy\b",
            r"\bdelayed\s+post.?hypoxic\s+leukoencephalopathy\b",
        ],
        "presentation_keywords": [
            r"\bhemiparesis\b", r"\baphasia\b", r"\bdysarthria\b",
            r"\bthrombolysis\b", r"\btpa\b", r"\bthrombectomy\b",
            r"\bnihss\b", r"\bwake.up\s+stroke\b",
            r"\bfacial\s+droop\b", r"\bunilateral\s+weakness\b",
        ],
    },
    "focal_epilepsy_temporal": {
        "abbreviation": "FEPI-TEMP",
        "diagnosis_keywords": [
            r"\btemporal\s+lobe\s+epilepsy\b", r"\bfocal\s+epilepsy\b",
            r"\bmesial\s+temporal\s+sclerosis\b", r"\bhippocampal\s+sclerosis\b",
            r"\btemporal\s+lobe\s+seizure\b", r"\bcomplex\s+partial\s+seizure\b",
            r"\bfocal\s+seizure\b", r"\bepilepsy\b",
            r"\bseizure\s+disorder\b",
        ],
        "presentation_keywords": [
            r"\bseizure\b", r"\bconvulsion\b", r"\beeg\b", r"\btonic.clonic\b",
            r"\baura\b", r"\bautomatism\b", r"\bpost.?ictal\b",
        ],
    },
    "multiple_sclerosis": {
        "abbreviation": "MS-RR",
        "diagnosis_keywords": [
            r"\bmultiple\s+sclerosis\b", r"\brelapsing.remitting\s+ms\b",
            r"\bdemyelinat(ing|ion)\b", r"\bclinically\s+isolated\s+syndrome\b",
            r"\bneuromyelitis\b", r"\boptic\s+neuritis\b.*ms\b",
            r"\btransverse\s+myelitis\b.*ms\b",
        ],
        "presentation_keywords": [
            r"\bdemyelinat\b", r"\boligoclonal\b", r"\bperiventricular\b",
            r"\boptic\s+neuritis\b", r"\btransverse\s+myelitis\b",
            r"\blhermitte\b", r"\binternuclear\s+ophthalmoplegia\b",
        ],
    },
    "alzheimers_early": {
        "abbreviation": "ALZ-EARLY",
        "diagnosis_keywords": [
            r"\balzheimer\b", r"\bearly.onset\s+dementia\b",
            r"\bamnestic\s+mild\s+cognitive\b", r"\bposterior\s+cortical\s+atrophy\b",
            r"\bvascular\s+dementia\b", r"\bdementia\b",
            r"\bwernicke\s+encephalopathy\b", r"\bhashimoto.s?\s+encephalopathy\b",
            r"\bprogressive\s+multifocal\s+leukoencephalopathy\b",
            r"\bnormal\s+pressure\s+hydrocephalus\b",
            r"\bcreutzfeldt.?jakob\b", r"\bprion\b",
            r"\bcognitive\s+(impairment|decline|dysfunction)\b",
            r"\bneurosyphilis\b", r"\bsubacute\s+combined\s+degeneration\b",
            r"\bsteroid\s+dementia\b",
        ],
        "presentation_keywords": [
            r"\bmemory\s+(loss|impairment|decline)\b", r"\bcognitive\s+decline\b",
            r"\bmmse\b", r"\bmoca\b", r"\bamyloid\b", r"\bhippocampal\s+atrophy\b",
            r"\bneuropsych\b", r"\bconfusion\b.*\bprogressive\b",
            r"\bforgetful\b", r"\bdisorientation\b",
        ],
    },
    "parkinsons": {
        "abbreviation": "PD",
        "diagnosis_keywords": [
            r"\bparkinson\b", r"\bparkinsoni(sm|an)\b",
            r"\bmultiple\s+system\s+atrophy\b", r"\bprogressive\s+supranuclear\s+palsy\b",
            r"\bcorticobasal\b", r"\blewy\s+body\b",
            r"\bessential\s+tremor\b", r"\bdrug.induced\s+parkinsonism\b",
            r"\bwilson.s?\s+disease\b", r"\bhuntington\b",
            r"\bchorea\b", r"\bdystoni(a|c)\b", r"\bataxia\b",
            r"\bspinocerebellar\b", r"\bfragile\s+x.*tremor\b",
            r"\borthostatic\s+tremor\b", r"\bhemichorea\b", r"\bhemiballism\b",
            r"\bcerebellar\s+ataxia\b",
        ],
        "presentation_keywords": [
            r"\btremor\b", r"\bbradykinesia\b", r"\brigidity\b",
            r"\bdatscan\b", r"\blevodopa\b", r"\bdopamin\b",
            r"\bcogwheel\b", r"\bfreezing\s+of\s+gait\b",
            r"\bmovement\s+disorder\b", r"\bgait\s+instability\b",
        ],
    },
    "brain_tumor_glioma": {
        "abbreviation": "GLIO-HG",
        "diagnosis_keywords": [
            r"\bglioblastoma\b", r"\bglioma\b", r"\bastrocytoma\b",
            r"\boligodendroglioma\b", r"\bmeningioma\b", r"\bbrain\s+(tumor|tumour|mass|neoplasm)\b",
            r"\bcns\s+(lymphoma|tumor|tumour)\b", r"\bmetastat.*brain\b",
            r"\bintracranial\s+(mass|neoplasm|tumor)\b",
        ],
        "presentation_keywords": [
            r"\bbrain\s+mass\b", r"\benhancing\s+lesion\b", r"\bintracranial\s+pressure\b",
            r"\bpapilledema\b", r"\bnew.onset\s+seizure\b.*mass\b",
        ],
    },
    "bacterial_meningitis": {
        "abbreviation": "BACT-MEN",
        "diagnosis_keywords": [
            r"\bbacterial\s+meningitis\b", r"\bmeningococcal\b", r"\bpneumococcal\s+meningitis\b",
            r"\blisteria\s+meningitis\b", r"\btuberculous\s+meningitis\b",
            r"\bmeningitis\b", r"\bmeningoencephalitis\b",
            r"\bviral\s+meningitis\b", r"\bfungal\s+meningitis\b",
            r"\bcryptococcal\s+meningitis\b",
        ],
        "presentation_keywords": [
            r"\bneck\s+stiffness\b", r"\bkernig\b", r"\bbrudzinski\b",
            r"\blumbar\s+puncture\b", r"\bcsf\s+pleocytosis\b",
            r"\bmeningeal\b", r"\bphotophobia\b.*fever\b",
        ],
    },
    "autoimmune_encephalitis_nmdar": {
        "abbreviation": "NMDAR-ENC",
        "diagnosis_keywords": [
            r"\banti.?nmda\b", r"\bnmdar\s+encephalitis\b",
            r"\bautoimmune\s+encephalitis\b", r"\blimbic\s+encephalitis\b",
            r"\banti.?lgi1\b", r"\banti.?caspr2\b", r"\banti.?gaba\b",
            r"\banti.?ampa\b", r"\bhashimoto\s+encephalopathy\b",
            r"\bparaneoplastic.*encephalitis\b",
        ],
        "presentation_keywords": [
            r"\bencephalitis\b.*autoimmune\b", r"\bpsychiatric.*seizure\b",
            r"\bdyskinesia.*encephalitis\b", r"\bteratoma\b",
            r"\borofacial\s+dyskinesia\b", r"\bextreme\s+delta\s+brush\b",
        ],
    },
    "functional_neurological_disorder": {
        "abbreviation": "FND",
        "diagnosis_keywords": [
            r"\bfunctional\s+neurological\b", r"\bconversion\s+disorder\b",
            r"\bpsychogenic\b", r"\bnon.?epileptic\s+(seizure|event|attack)\b",
            r"\bfunctional\s+(weakness|tremor|movement|dystonia|gait)\b",
            r"\bsomatoform\b", r"\bdissociative\b",
            r"\bfactitious\b", r"\bmunchausen\b", r"\bmalingering\b",
            r"\bpsychogenic\s+(polydipsia|movement|tremor|nonepileptic|dystonia)\b",
            r"\bnon.?organic\b", r"\bmedically\s+unexplained\b",
            r"\bsomatic\s+symptom\s+disorder\b",
        ],
        "presentation_keywords": [
            r"\bhoover\b", r"\bdragging\s+gait\b",
            r"\bdistractib(le|ility)\b", r"\bla\s+belle\s+indiff[eé]rence\b",
            r"\bgive.?way\s+weakness\b", r"\bentrainment\b",
            r"\binconsisten(t|cy)\b.*\bneurological\b",
        ],
    },
    "syncope_cardiac": {
        "abbreviation": "SYNC-CARD",
        "diagnosis_keywords": [
            r"\bcardiac\s+syncope\b", r"\bsyncope\b",
            r"\bbrugada\b", r"\blong\s+qt\b", r"\bwpw\b",
            r"\bcomplete\s+(heart|av)\s+block\b", r"\batrioventricular\s+block\b",
            r"\bhypertrophic\s+cardiomyopathy\b",
            r"\barvc\b", r"\barrhythmogenic\b",
            r"\bvasovagal\b", r"\bneurocardiogenic\b",
            r"\bsick\s+sinus\b", r"\bventricular\s+tachycardia\b",
            r"\bsupraventricular\s+tachycardia\b",
            r"\baortic\s+stenosis\b", r"\bcardiac\s+arrest\b",
            r"\bsudden\s+cardiac\s+death\b",
            r"\btorsade\b", r"\bventricular\s+fibrillation\b",
        ],
        "presentation_keywords": [
            r"\bsyncope\b", r"\bloss\s+of\s+consciousness\b", r"\bpresyncope\b",
            r"\btilt\s+table\b", r"\bholter\b", r"\bpalpitation\b",
            r"\bcollapse\b", r"\bblack.?out\b",
        ],
    },
    "guillain_barre": {
        "abbreviation": "GBS",
        "diagnosis_keywords": [
            r"\bguillain.?barr[eé]\b", r"\bacute\s+inflammatory\s+demyelinating\b",
            r"\bAIDP\b", r"\bacute\s+motor\s+axonal\s+neuropathy\b", r"\bAMAN\b",
            r"\bMiller\s+Fisher\b", r"\banti.?GQ1b\b", r"\bascending\s+paralysis\b",
        ],
        "presentation_keywords": [
            r"\bareflexia\b", r"\bascending\s+weakness\b",
            r"\balbumin[o-]cytologic\s+dissociation\b", r"\bcranial\s+neuropathy\b",
            r"\brespiratory\s+failure.*weakness\b",
        ],
    },
    "myasthenia_gravis": {
        "abbreviation": "MG",
        "diagnosis_keywords": [
            r"\bmyasthenia\s+gravis\b", r"\blambert.?eaton\b",
            r"\bneuromuscular\s+junction\b", r"\bacetylcholine\s+receptor\b",
            r"\bMuSK\b", r"\bthymoma.*myasthenia\b",
            r"\bocular\s+myasthenia\b", r"\bmyasthenic\s+crisis\b",
        ],
        "presentation_keywords": [
            r"\bptosis\b", r"\bdiplopia\b", r"\bfatigable\s+weakness\b",
            r"\bbulbar\b", r"\bdysphagia.*weakness\b", r"\bice\s+pack\s+test\b",
        ],
    },
    "subarachnoid_hemorrhage": {
        "abbreviation": "SAH",
        "diagnosis_keywords": [
            r"\bsubarachnoid\s+hemorrhage\b", r"\bsubarachnoid\s+haemorrhage\b",
            r"\baneurysm.*rupture\b", r"\bcerebral\s+aneurysm\b",
            r"\bberry\s+aneurysm\b", r"\bthunderclap\s+headache.*aneurysm\b",
            r"\bSAH\b", r"\bHunt\s+and\s+Hess\b", r"\bFisher\s+grade\b",
        ],
        "presentation_keywords": [
            r"\bthunderclap\s+headache\b", r"\bworst\s+headache\b",
            r"\bsudden\s+onset\s+headache\b", r"\bnuchal\s+rigidity.*headache\b",
            r"\bsentinel\s+headache\b",
        ],
    },
    "migraine_with_aura": {
        "abbreviation": "MIG-AURA",
        "diagnosis_keywords": [
            r"\bmigraine\s+with\s+aura\b", r"\bmigraine.*visual\b",
            r"\bhemiplegic\s+migraine\b", r"\bretinal\s+migraine\b",
            r"\bmigraine\s+with\s+brainstem\s+aura\b", r"\bbasilar\s+migraine\b",
            r"\bophthalmoplegic\s+migraine\b", r"\bMELAS.*migraine\b",
        ],
        "presentation_keywords": [
            r"\bscintillating\s+scotoma\b", r"\bvisual\s+aura\b",
            r"\bfortification\s+spectra\b", r"\bmigraine\s+aura\b",
            r"\bspreading.*visual\b",
        ],
    },
    "frontotemporal_dementia": {
        "abbreviation": "FTD",
        "diagnosis_keywords": [
            r"\bfrontotemporal\s+dementia\b", r"\bbehavioral\s+variant\s+FTD\b",
            r"\bPick.s\s+disease\b", r"\bprimary\s+progressive\s+aphasia\b",
            r"\bsemantic\s+dementia\b", r"\bprogressive\s+nonfluent\s+aphasia\b",
            r"\bFTD.ALS\b", r"\bC9orf72\b",
        ],
        "presentation_keywords": [
            r"\bdisinhibition\b", r"\bapathy.*dementia\b",
            r"\bpersonality\s+change.*cognitive\b", r"\bfrontal\s+atrophy\b",
            r"\btemporal\s+atrophy.*language\b",
        ],
    },
    "status_epilepticus": {
        "abbreviation": "SE",
        "diagnosis_keywords": [
            r"\bstatus\s+epilepticus\b", r"\brefractory\s+status\s+epilepticus\b",
            r"\bsuper.?refractory\b", r"\bnon.?convulsive\s+status\s+epilepticus\b",
            r"\bNCSE\b", r"\bconvulsive\s+status\b",
        ],
        "presentation_keywords": [
            r"\bprolonged\s+seizure\b", r"\bcontinuous\s+seizure\b",
            r"\bseizure.*>\s*5\s+min\b", r"\bunresponsive.*seizure\b",
        ],
    },
    "peripheral_neuropathy": {
        "abbreviation": "PERI-NEURO",
        "diagnosis_keywords": [
            r"\bperipheral\s+neuropathy\b", r"\bdiabetic\s+neuropathy\b",
            r"\bCIDP\b", r"\bchronic\s+inflammatory\s+demyelinating\b",
            r"\bCharcot.?Marie.?Tooth\b", r"\bhereditary\s+neuropathy\b",
            r"\bvasculitic\s+neuropathy\b", r"\btoxic\s+neuropathy\b",
            r"\balcoholic\s+neuropathy\b", r"\bsmall\s+fiber\s+neuropathy\b",
        ],
        "presentation_keywords": [
            r"\bnumbness.*feet\b", r"\btingling.*stocking\b",
            r"\bdistal\s+weakness\b", r"\bnerve\s+conduction\b",
            r"\bEMG.*neuropathy\b", r"\bareflexia.*distal\b",
        ],
    },
    "normal_pressure_hydrocephalus": {
        "abbreviation": "NPH",
        "diagnosis_keywords": [
            r"\bnormal\s+pressure\s+hydrocephalus\b", r"\bNPH\b",
            r"\bHakim.s\s+triad\b", r"\bcommunicating\s+hydrocephalus\b",
            r"\bidiopathic\s+NPH\b", r"\bshunt\s+responsive\b",
        ],
        "presentation_keywords": [
            r"\bgait\s+apraxia.*incontinence\b", r"\bmagnetic\s+gait\b",
            r"\bventriculomegaly\b", r"\bgait.*cognitive.*urinary\b",
        ],
    },
    "hepatic_encephalopathy": {
        "abbreviation": "HEP-ENC",
        "diagnosis_keywords": [
            r"\bhepatic\s+encephalopathy\b", r"\bhyperammonemia\b",
            r"\bporto.?systemic\s+encephalopathy\b", r"\bhepatic\s+coma\b",
            r"\bliver\s+failure.*encephalopathy\b", r"\bcirrhosis.*encephalopathy\b",
            r"\bammonia.*encephalopathy\b",
        ],
        "presentation_keywords": [
            r"\basterixis\b", r"\btriphasic\s+waves\b",
            r"\bammonia.*elevated\b", r"\bhepatic\s+flap\b",
            r"\bliver.*confusion\b",
        ],
    },
    "amyotrophic_lateral_sclerosis": {
        "abbreviation": "ALS",
        "diagnosis_keywords": [
            r"\bamyotrophic\s+lateral\s+sclerosis\b", r"\bALS\b",
            r"\bmotor\s+neuron\s+disease\b", r"\bprogressive\s+muscular\s+atrophy\b",
            r"\bprimary\s+lateral\s+sclerosis\b", r"\bprogressive\s+bulbar\s+palsy\b",
            r"\bLou\s+Gehrig\b",
        ],
        "presentation_keywords": [
            r"\bfasciculation.*weakness\b", r"\bupper.*lower\s+motor\s+neuron\b",
            r"\btongue\s+fasciculation\b", r"\bsplit\s+hand\b",
            r"\bEl\s+Escorial\b",
        ],
    },
}

# Minimum case_prompt length to be considered a quality seed
MIN_PROMPT_LENGTH = 500
# Minimum diagnostic_reasoning length
MIN_REASONING_LENGTH = 300


def score_seed(row: dict, condition_key: str) -> float:
    """Score a candidate seed case for quality and relevance.

    Higher score = better seed. Components:
    - Diagnosis keyword match strength (0-3)
    - Presentation keyword match count (0-2)
    - Case prompt length bonus (0-1)
    - Reasoning richness bonus (0-1)
    """
    cfg = CONDITION_FILTERS[condition_key]
    diagnosis = row.get("final_diagnosis", "").lower()
    prompt = row.get("case_prompt", "").lower()
    reasoning = row.get("diagnostic_reasoning", "").lower()

    score = 0.0

    # Diagnosis keyword matches (highest weight)
    diag_matches = sum(1 for kw in cfg["diagnosis_keywords"] if re.search(kw, diagnosis, re.IGNORECASE))
    score += min(diag_matches * 1.5, 4.5)

    # Presentation keyword matches
    pres_matches = sum(1 for kw in cfg["presentation_keywords"] if re.search(kw, prompt, re.IGNORECASE))
    pres_matches += sum(0.5 for kw in cfg["presentation_keywords"] if re.search(kw, reasoning, re.IGNORECASE))
    score += min(pres_matches * 0.3, 2.0)

    # Case prompt length bonus (longer = richer clinical detail)
    prompt_len = len(row.get("case_prompt", ""))
    if prompt_len > 2000:
        score += 1.0
    elif prompt_len > 1000:
        score += 0.5

    # Reasoning richness
    reasoning_len = len(row.get("diagnostic_reasoning", ""))
    if reasoning_len > 2000:
        score += 1.0
    elif reasoning_len > 1000:
        score += 0.5

    return score


def matches_condition(row: dict, condition_key: str) -> bool:
    """Check if a case matches a condition based on diagnosis keywords."""
    cfg = CONDITION_FILTERS[condition_key]
    diagnosis = row.get("final_diagnosis", "")
    prompt = row.get("case_prompt", "")

    # Must match at least one diagnosis keyword
    diag_match = any(
        re.search(kw, diagnosis, re.IGNORECASE)
        for kw in cfg["diagnosis_keywords"]
    )
    if diag_match:
        return True

    # Fallback: strong presentation match + partial diagnosis match
    pres_matches = sum(
        1 for kw in cfg["presentation_keywords"]
        if re.search(kw, prompt, re.IGNORECASE)
    )
    return pres_matches >= 3


def assign_difficulty(idx: int, total: int) -> str:
    """Assign difficulty based on position in ranked list.

    Top seeds → straightforward (clearest cases)
    Middle → moderate
    Bottom → diagnostic_puzzle (more ambiguous/complex)
    """
    frac = idx / total if total > 0 else 0
    if frac < 0.4:
        return "straightforward"
    elif frac < 0.7:
        return "moderate"
    else:
        return "diagnostic_puzzle"


def main():
    parser = argparse.ArgumentParser(description="Filter MedCaseReasoning for NeuroBench seeds")
    parser.add_argument("--output", default="dataset-generation/seeds", help="Output directory for seed JSONs")
    parser.add_argument("--target-per-condition", type=int, default=30, help="Target seeds per condition")
    parser.add_argument("--exclude-pmcids", default="data/neurobench/cases", help="Directory of existing cases to exclude PMCIDs from")
    parser.add_argument("--dry-run", action="store_true", help="Print stats without writing files")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    # ── Load existing PMCIDs to exclude ──
    exclude_pmcids: set[str] = set()
    exclude_dir = Path(args.exclude_pmcids)
    if exclude_dir.exists():
        for f in exclude_dir.glob("*.json"):
            try:
                with open(f) as fh:
                    case = json.load(fh)
                    pmcid = case.get("metadata", {}).get("source_pmcid", "")
                    if pmcid:
                        exclude_pmcids.add(pmcid)
            except (json.JSONDecodeError, KeyError):
                continue
    logger.info("Excluding %d PMCIDs from existing v2 cases", len(exclude_pmcids))

    # ── Load MedCaseReasoning (both train + test splits) ──
    logger.info("Loading MedCaseReasoning from HuggingFace (train + test)...")
    from datasets import concatenate_datasets
    ds_train = load_dataset("zou-lab/MedCaseReasoning", split="train")
    ds_test = load_dataset("zou-lab/MedCaseReasoning", split="test")
    ds = concatenate_datasets([ds_train, ds_test])
    logger.info("Loaded %d cases (%d train + %d test)", len(ds), len(ds_train), len(ds_test))

    # ── Filter and score ──
    candidates: dict[str, list[tuple[float, dict]]] = defaultdict(list)
    seen_pmcids_per_condition: dict[str, set] = defaultdict(set)
    total_matches = 0

    for row in ds:
        pmcid = row.get("pmcid", "")

        # Skip already-used PMCIDs
        if pmcid in exclude_pmcids:
            continue

        # Skip short cases
        if len(row.get("case_prompt", "")) < MIN_PROMPT_LENGTH:
            continue
        if len(row.get("diagnostic_reasoning", "")) < MIN_REASONING_LENGTH:
            continue

        # Check each condition
        for condition_key in CONDITION_FILTERS:
            if matches_condition(row, condition_key):
                # Avoid same PMCID in same condition
                if pmcid in seen_pmcids_per_condition[condition_key]:
                    continue
                seen_pmcids_per_condition[condition_key].add(pmcid)

                score = score_seed(row, condition_key)
                candidates[condition_key].append((score, {
                    "pmcid": pmcid,
                    "title": row.get("title", ""),
                    "journal": row.get("journal", ""),
                    "article_link": row.get("article_link", ""),
                    "publication_date": row.get("publication_date", ""),
                    "case_prompt": row.get("case_prompt", ""),
                    "diagnostic_reasoning": row.get("diagnostic_reasoning", ""),
                    "final_diagnosis": row.get("final_diagnosis", ""),
                }))
                total_matches += 1

    logger.info("Total condition matches: %d", total_matches)

    # ── Print stats and select top seeds ──
    output_dir = Path(args.output)
    total_selected = 0

    for condition_key in sorted(CONDITION_FILTERS.keys()):
        abbrev = CONDITION_FILTERS[condition_key]["abbreviation"]
        cands = candidates.get(condition_key, [])
        # Sort by score descending
        cands.sort(key=lambda x: x[0], reverse=True)

        target = args.target_per_condition
        selected = cands[:target]

        logger.info(
            "%s (%s): %d candidates, selecting %d (scores: %.1f - %.1f)",
            condition_key, abbrev,
            len(cands), len(selected),
            selected[0][0] if selected else 0,
            selected[-1][0] if selected else 0,
        )

        if args.dry_run:
            for i, (score, seed) in enumerate(selected[:5]):
                logger.info(
                    "  [%.1f] %s — %s (%d chars)",
                    score, seed["pmcid"], seed["final_diagnosis"][:60], len(seed["case_prompt"]),
                )
            if len(selected) > 5:
                logger.info("  ... and %d more", len(selected) - 5)
            total_selected += len(selected)
            continue

        # Write seed files
        condition_dir = output_dir / condition_key
        condition_dir.mkdir(parents=True, exist_ok=True)

        # Count existing v2 cases for this condition to determine starting number
        # v2 cases go up to R{S|M|P}10, so new seeds start at 11
        difficulty_counters = {"straightforward": 0, "moderate": 0, "diagnostic_puzzle": 0}

        for i, (score, seed) in enumerate(selected):
            difficulty = assign_difficulty(i, len(selected))
            difficulty_counters[difficulty] += 1

            diff_letter = {"straightforward": "S", "moderate": "M", "diagnostic_puzzle": "P"}[difficulty]
            # Offset from existing v2 (which goes up to 10 per difficulty)
            case_num = difficulty_counters[difficulty] + 10  # v2 used 01-10
            case_id = f"{abbrev}-R{diff_letter}{case_num:02d}"

            seed_out = {
                **seed,
                "condition_key": condition_key,
                "case_id": case_id,
                "difficulty": difficulty,
                "score": round(score, 2),
            }

            seed_path = condition_dir / f"{case_id}.json"
            with open(seed_path, "w") as fh:
                json.dump(seed_out, fh, indent=2, ensure_ascii=False)

        n_s = difficulty_counters["straightforward"]
        n_m = difficulty_counters["moderate"]
        n_p = difficulty_counters["diagnostic_puzzle"]
        logger.info("  Written: %dS + %dM + %dP = %d seeds", n_s, n_m, n_p, sum(difficulty_counters.values()))
        total_selected += sum(difficulty_counters.values())

    logger.info("Total seeds selected: %d across %d conditions", total_selected, len(CONDITION_FILTERS))

    if not args.dry_run:
        logger.info("Seeds written to %s", output_dir)


if __name__ == "__main__":
    main()
