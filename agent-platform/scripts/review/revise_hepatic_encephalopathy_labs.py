"""Make the reviewer-2 core HE laboratory panel and its results mutually reachable."""
from __future__ import annotations
import argparse,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]; DEFAULT_CASES=ROOT/'data'/'neurobench'/'cases'
CORE=['CBC','CMP','ammonia','magnesium','lactate','coagulation','TSH','zinc','toxicology']

def row(test,value,unit,ref):
 return {'test':test,'value':value,'unit':unit,'reference_range':ref,'is_abnormal':False,'clinical_significance':None}

def revise(case):
 gt=case['ground_truth']; labs=[a for a in gt['optimal_actions'] if a.get('tool_name')=='interpret_labs']
 if not labs: raise ValueError(case['case_id'])
 primary=max(labs,key=lambda a:len((a.get('tool_parameters') or {}).get('panels',[])))
 panels=primary.setdefault('tool_parameters',{}).setdefault('panels',[])
 for p in CORE:
  if p not in panels: panels.append(p)
 primary['action']='Obtain the core HE/precipitant panel: CBC, electrolytes/renal/liver function, glucose, ammonia, magnesium, lactate, INR/coagulation, CRP, TSH, zinc and blood alcohol/urine drug screen; add phenotype-specific tests only when indicated.'
 primary['expected_finding']='Metabolic, infectious, endocrine, nutritional or toxic precipitant, interpreted with ammonia as supportive rather than a severity marker.'
 out=case['initial_tool_outputs'].get('labs')
 if out:
  ps=out.setdefault('panels',{})
  ps.setdefault('TSH',[row('TSH',2.1,'mIU/L','0.4-4.0')])
  ps.setdefault('Zinc',[row('Serum zinc',82,'µg/dL','60-120')])
  ps.setdefault('Toxicology',[row('Blood ethanol','Not detected','mg/dL','Not detected'),row('Urine drug screen','Negative','', 'Negative')])
 case['metadata']['last_revised']='2026-08-10'
 case['metadata']['revision_reason']='Reviewer 2 HE audit: core endocrine, zinc and toxicology studies are now named in the order and available in the laboratory output; phenotype-specific additions retained.'

def main():
 p=argparse.ArgumentParser();p.add_argument('--cases',type=Path,default=DEFAULT_CASES);p.add_argument('--check',action='store_true');a=p.parse_args();n=0
 for f in sorted(a.cases.glob('HEP-ENC-*.json')):
  c=json.loads(f.read_text());b=json.dumps(c,sort_keys=True);revise(c)
  if json.dumps(c,sort_keys=True)!=b:
   n+=1
   if not a.check:f.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n')
 print(f'hepatic-encephalopathy laboratory cases changed: {n}')
 if a.check and n:raise SystemExit(1)
if __name__=='__main__':main()
