"""Rebuild temporal-lobe epilepsy SFT traces around the reviewed staged pathway."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = ROOT / "training_data" / "gold_trajectories" / "trajectories.jsonl"
CASES = ROOT / "data" / "neurobench" / "cases"


def _pair(name: str, args: dict[str, Any], output: dict[str, Any], thought: str) -> list[dict[str, Any]]:
    return [{"role": "assistant", "content": f"<think>\n{thought}\n</think>",
             "tool_calls": [{"type": "function", "function": {"name": name, "arguments": args}}]},
            {"role": "tool", "content": json.dumps(output, indent=2, ensure_ascii=False)}]


def _action(case: dict[str, Any], tool: str, key: str | None = None, value: str | None = None) -> dict[str, Any] | None:
    for row in case["ground_truth"]["optimal_actions"]:
        if row.get("tool_name") != tool: continue
        if key and row.get("tool_parameters", {}).get(key) != value: continue
        return row
    return None


def _output(case: dict[str, Any], tool: str, key: str | None = None, value: str | None = None) -> dict[str, Any]:
    ikey = {"analyze_eeg":"eeg", "analyze_brain_mri":"mri", "order_ct_scan":"ct", "interpret_labs":"labs",
            "analyze_ecg":"ecg", "order_specialized_test":"specialized_test", "order_body_imaging":"body_imaging",
            "search_medical_literature":"literature_search", "check_drug_interactions":"drug_interactions"}.get(tool)
    initial = case["initial_tool_outputs"].get(ikey) if ikey else None
    if initial is not None and (not key or initial.get(key) == value): return initial
    for row in case["followup_outputs"]:
        out = row.get("output") or {}
        if row.get("tool_name") == tool and (not key or out.get(key) == value): return out
    raise ValueError(f"{case['case_id']}: missing {tool} {key}={value}")


def _clean_final(text: str, case: dict[str, Any], calls: list[tuple[str,str|None]]) -> str:
    tools={x[0] for x in calls}; eeg={x[1] for x in calls if x[0]=='analyze_eeg'}
    lines=[]
    for line in text.splitlines():
        low=line.lower()
        if any(x in low for x in ('echocardiogram','holter','tilt-table','tilt table')): continue
        if 'video-eeg' in low and 'video' not in eeg: continue
        if 'ambulatory eeg' in low and 'ambulatory' not in eeg: continue
        if 'sleep-deprived' in low and 'sleep_deprived' not in eeg: continue
        if 'continuous eeg' in low and 'continuous_icu' not in eeg: continue
        if 'ecg' in low and 'analyze_ecg' not in tools: continue
        if 'lab' in low and 'interpret_labs' not in tools: continue
        if 'mri' in low and 'analyze_brain_mri' not in tools: continue
        if ('pulmonary embol' in low or 'ctpa' in low) and 'order_body_imaging' not in tools: continue
        lines.append(line)
    out=re.sub(r'\n{3,}','\n\n','\n'.join(lines)).strip()
    primary=case['ground_truth']['primary_diagnosis']
    out=re.sub(r'(### Primary Diagnosis\s*\n)[^\n]+',rf'\g<1>{primary}',out,count=1)
    if case['case_id']=='FEPI-TEMP-P04': out=out.replace('brain MRI','non-contrast head CT').replace('MRI','CT')
    return out or f"### Primary Diagnosis\n{primary}\n\nThe reviewed clinical, EEG and structural pathway supports this diagnosis."


def revise(row: dict[str, Any], case: dict[str, Any]) -> bool:
    if row.get('condition')!='focal_epilepsy_temporal': return False
    before=json.dumps(row,sort_keys=True); original=row['messages']; differential=row.get('style')=='differential_reasoned'
    messages=[dict(m) for m in original if m.get('role') in {'system','user'}][:2]
    final=next((m.get('content','') for m in reversed(original) if m.get('role')=='assistant' and not m.get('tool_calls')),'')
    calls: list[tuple[str,str|None]]=[]

    body=_action(case,'order_body_imaging')
    if body:
        messages+=_pair('order_body_imaging',{'clinical_context':body['action'],**body['tool_parameters']},_output(case,'order_body_imaging'),
                        'Hemoptysis, dyspnoea and unilateral calf pain are a concurrent emergency. I must evaluate PE in parallel rather than substitute a generic echo or Holter.')
        calls.append(('order_body_imaging',body['tool_parameters']['study']))

    types=[t for t in ('routine','sleep_deprived','ambulatory','video','continuous_icu') if _action(case,'analyze_eeg','eeg_type',t)]
    if not types:
        selected=[]
    elif not differential:
        selected=[next((t for t in ('routine','video','continuous_icu') if t in types),types[0])]
    else:
        # A gold trace cannot call one tool twice. The two styles therefore teach distinct stages
        # of the reviewed escalation rather than pretending the staged pathway is one call.
        selected=[next((t for t in ('ambulatory','sleep_deprived','video','continuous_icu','routine') if t in types),types[0])]
    for t in selected:
        thought={
            'routine':'The history suggests an epileptic seizure, so an awake routine EEG supports classification; a normal result will not exclude epilepsy.',
            'sleep_deprived':'The routine trace was normal or equivocal. The reviewed next step is sleep-deprived EEG after discussing provocation risks.',
            'ambulatory':'Routine and sleep-deprived studies remain non-diagnostic, so ambulatory EEG is the staged next step to capture a habitual event.',
            'video':'Habitual-event capture, PNES differentiation or presurgical localization requires synchronized prolonged video-EEG.',
            'continuous_icu':'This patient may be in non-convulsive status; continuous ICU EEG is the acute exception and cannot be generalized to routine TLE.',
        }[t]
        messages+=_pair('analyze_eeg',{'clinical_context':_action(case,'analyze_eeg','eeg_type',t)['action'],'eeg_type':t},
                        _output(case,'analyze_eeg','eeg_type',t),thought); calls.append(('analyze_eeg',t))

    ecg=_action(case,'analyze_ecg')
    if ecg:
        messages+=_pair('analyze_ecg',{'clinical_context':'first suspected seizure or transient loss of consciousness; identify a cardiac mimic'},_output(case,'analyze_ecg'),
                        'A 12-lead ECG is appropriate in a first suspected seizure to identify a cardiac mimic; it is not an epilepsy test.')
        calls.append(('analyze_ecg',None))

    labs=_action(case,'interpret_labs')
    if labs:
        dem=case['patient']['demographics']
        messages+=_pair('interpret_labs',{'clinical_context':labs['action'],'panels':labs['tool_parameters']['panels'],
                        'patient_age':dem['age'],'patient_sex':dem['sex']},_output(case,'interpret_labs'),
                        'These optional labs answer a case-specific provocation, drug-level or concurrent-emergency question; there is no routine epilepsy panel.')
        calls.append(('interpret_labs',None))

    mri=_action(case,'analyze_brain_mri')
    if mri:
        messages+=_pair('analyze_brain_mri',{'clinical_context':'identify a structural epileptogenic cause using a dedicated HARNESS-style epilepsy protocol',**mri['tool_parameters']},
                        _output(case,'analyze_brain_mri'),'Structural imaging must use a dedicated epilepsy protocol capable of showing hippocampal sclerosis, dysplasia, tumour or vascular lesions.')
        calls.append(('analyze_brain_mri',None))
    else:
        ct=_action(case,'order_ct_scan'); assert ct
        messages+=_pair('order_ct_scan',{'clinical_context':'MRI unavailable because of severe claustrophobia; structural epilepsy assessment with stated limitations','contrast':False},
                        _output(case,'order_ct_scan'),'MRI is unavailable, so CT is the reviewed alternative; it cannot exclude subtle focal cortical dysplasia or hippocampal sclerosis.')
        calls.append(('order_ct_scan',None))

    neuro=_action(case,'order_specialized_test','test_type','neuropsych_battery')
    if neuro and differential:
        messages+=_pair('order_specialized_test',{'clinical_context':'tertiary presurgical cognitive lateralization and resection-risk assessment','test_type':'neuropsych_battery'},
                        _output(case,'order_specialized_test','test_type','neuropsych_battery'),
                        'Neuropsychology is optional here because this is a tertiary surgical evaluation, not routine focal-epilepsy diagnosis.')
        calls.append(('order_specialized_test','neuropsych_battery'))

    for tool in ('check_drug_interactions','search_medical_literature'):
        action=_action(case,tool)
        if not action: continue
        if tool=='check_drug_interactions':
            args=dict(action.get('tool_parameters',{})); args.setdefault('drug','antiepileptic therapy')
            thought='Before starting or changing antiseizure therapy, check interactions relevant to this patient.'
        else:
            args=dict(action.get('tool_parameters',{})); args.setdefault('query','focal temporal epilepsy diagnosis and treatment'); args.setdefault('max_results',3)
            thought='Check the evidence relevant to the active classification or treatment question.'
        messages+=_pair(tool,args,_output(case,tool),thought); calls.append((tool,None))

    messages.append({'role':'assistant','content':_clean_final(final,case,calls)})
    row['messages']=messages; names=[x[0] for x in calls]; row['tools_called']=list(dict.fromkeys(names)); row['num_tool_calls']=len(names)
    return json.dumps(row,sort_keys=True)!=before


def main() -> None:
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=DEFAULT_INPUT);p.add_argument('--check',action='store_true');args=p.parse_args()
    cases={p.stem:json.loads(p.read_text()) for p in CASES.glob('FEPI-TEMP-*.json')}; rows=[json.loads(x) for x in args.input.read_text().splitlines() if x.strip()]
    changed=sum(revise(r,cases[r['case_id']]) for r in rows if r.get('condition')=='focal_epilepsy_temporal')
    rendered=''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows);print(f'Focal epilepsy trajectories changed: {changed}')
    if args.check and changed: raise SystemExit(1)
    if not args.check: args.input.write_text(rendered)


if __name__=='__main__':main()
