"""Rebuild meningitis traces around cultures, LP and no-treatment-delay sequencing."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[3]
DEFAULT_INPUT=ROOT/"training_data"/"gold_trajectories"/"trajectories.jsonl"
CASES=ROOT/"data"/"neurobench"/"cases"
def pair(n,a,o,t): return [{"role":"assistant","content":f"<think>\n{t}\n</think>","tool_calls":[{"type":"function","function":{"name":n,"arguments":a}}]},{"role":"tool","content":json.dumps(o,indent=2,ensure_ascii=False)}]
def acts(c,t): return [a for a in c["ground_truth"]["optimal_actions"] if a.get("tool_name")==t]
def output(c,t):
    key={"interpret_labs":"labs","analyze_csf":"csf","order_ct_scan":"ct","analyze_brain_mri":"mri","analyze_eeg":"eeg","order_microbiology":"microbiology","search_medical_literature":"literature_search","check_drug_interactions":"drug_interactions"}[t]
    if c["initial_tool_outputs"].get(key): return c["initial_tool_outputs"][key]
    return next(x["output"] for x in c["followup_outputs"] if x.get("tool_name")==t)
def has(c,t):
    try: output(c,t)
    except (StopIteration,KeyError,TypeError): return False
    return True
def call(ms,names,c,t,a,thought): ms.extend(pair(t,a,output(c,t),thought)); names.append(t)
def revise(r,c):
    if r.get("condition")!="bacterial_meningitis": return False
    before=json.dumps(r,sort_keys=True); diff=r.get("style")=="differential_reasoned"; ms=[dict(x) for x in r["messages"] if x.get("role") in {"system","user"}][:2]; names=[]
    micro=acts(c,"order_microbiology")[0]
    call(ms,names,c,"order_microbiology",{"clinical_context":micro["action"],"specimen":"blood_culture","tests":["culture","gram_stain","susceptibility"],"before_antimicrobials":True},"Draw blood cultures promptly before treatment if possible, but never delay empirical antimicrobials for sampling or imaging.")
    lab=acts(c,"interpret_labs")[0]; dem=c["patient"]["demographics"]
    call(ms,names,c,"interpret_labs",{"clinical_context":lab["action"],"panels":lab["tool_parameters"]["panels"],"patient_age":dem["age"],"patient_sex":dem["sex"]},"Blood glucose is paired with CSF; blood studies support safety and sepsis assessment, not confirmation, and do not defer LP or treatment.")
    ct=acts(c,"order_ct_scan")
    if ct and has(c,"order_ct_scan"):
        call(ms,names,c,"order_ct_scan",{"clinical_context":ct[0]["action"],"contrast":False,"angiography":False},"This case has a stated safety indication for NCCT before LP; empirical antimicrobials proceed if imaging would delay them.")
    csf=acts(c,"analyze_csf")[0]
    call(ms,names,c,"analyze_csf",{"clinical_context":csf["action"],"special_tests":["meningitis_panel"]},"LP must report opening pressure, appearance, differential cells, RBC, protein, paired glucose, Gram stain/culture-susceptibility and relevant PCR with pre/post-antibiotic timing.")
    if diff:
        mri=acts(c,"analyze_brain_mri")
        if mri and has(c,"analyze_brain_mri"):
            call(ms,names,c,"analyze_brain_mri",{"clinical_context":mri[0]["action"],"protocol":"standard","contrast":True},"MRI is reserved for this case's suspected complication or atypical alternative; it is not initial diagnostic imaging for ordinary bacterial meningitis.")
        for t,thought in (("check_drug_interactions","Antibiotic and dexamethasone safety review supports treatment but not diagnosis."),("search_medical_literature","A focused guideline check can inform organism-specific management but cannot delay treatment.")):
            aa=acts(c,t)
            if aa and has(c,t):
                if t=="check_drug_interactions": args={"drug":"empiric meningitis regimen","current_medications":[]}
                else: args={"query":"WHO 2025 bacterial meningitis treatment", "max_results":3}
                call(ms,names,c,t,args,thought)
    primary=c["ground_truth"]["primary_diagnosis"]
    ms.append({"role":"assistant","content":f"### Primary Diagnosis\n{primary}\n\nBlood cultures and empirical therapy must not wait for LP or imaging. The CSF result is interpreted with its sampling timing, paired blood glucose, Gram stain/culture-susceptibility and relevant PCR. MRI is reserved for complications or failure to improve."})
    r["messages"]=ms; r["tools_called"]=names; r["num_tool_calls"]=len(names)
    return json.dumps(r,sort_keys=True)!=before
def main():
    p=argparse.ArgumentParser();p.add_argument("--input",type=Path,default=DEFAULT_INPUT);p.add_argument("--check",action="store_true");a=p.parse_args(); cases={x.stem:json.loads(x.read_text()) for x in CASES.glob("BACT-MEN-*.json")}; rows=[json.loads(x) for x in a.input.read_text().splitlines() if x.strip()]; changed=sum(revise(r,cases[r["case_id"]]) for r in rows if r.get("condition")=="bacterial_meningitis"); print(f"bacterial-meningitis trajectories changed: {changed}");
    if a.check and changed: raise SystemExit(1)
    if not a.check:a.input.write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in rows))
if __name__=="__main__":main()
