"""Every number the review app shows a clinician, checked against the 600 case files.

`condition_tool_guidance.yaml` answers each of the reviewers' 91 comments with a sentence like
"required in all 30 cases" or "no case orders CSF studies". Those sentences are shown to the
two neurologists next to their own text, so a stale one is worse than no answer: it tells a
clinician the dataset behaves in a way it does not, in the one place they have no way to check.

This test is deliberately brittle. It re-derives every quantified claim from the case files, so
retiering a single action fails it — which is the point: the claim in the app has to be edited
at the same time as the data, in `scripts/review/build_condition_tool_guidance.py`. One of these
claims was wrong when it was written (the syncope echocardiogram is required in 29 cases, not
30, because a Brugada case correctly has it as recommended) and this is what caught it.
"""
from __future__ import annotations
import json, glob, collections

CASES = collections.defaultdict(list)
for f in sorted(glob.glob('data/neurobench/cases/*.json')):
    d = json.load(open(f))
    CASES[d['condition']].append(d)

def cases_with(cond, tool, cats=None, param=None):
    """case ids where `tool` appears at one of `cats`, optionally with `param` in its parameters."""
    out = set()
    for d in CASES[cond]:
        for a in d['ground_truth']['optimal_actions']:
            if a.get('tool_name') != tool: continue
            if cats and a.get('category') not in cats: continue
            if param and param not in json.dumps(a.get('tool_parameters') or {}): continue
            out.add(d['case_id'])
    return out

def n_actions(cond, tool, cats=None, param=None):
    n = 0
    for d in CASES[cond]:
        for a in d['ground_truth']['optimal_actions']:
            if a.get('tool_name') != tool: continue
            if cats and a.get('category') not in cats: continue
            if param and param not in json.dumps(a.get('tool_parameters') or {}): continue
            n += 1
    return n

R = 'required'; C = 'recommended'; O = 'optional'
CLAIMS = [
    # (label, actual, expected)
    ('als/csf recommended in all 30',            len(cases_with('als','analyze_csf',[C])), 30),
    ('als/csf never required',                   len(cases_with('als','analyze_csf',[R])), 0),
    ('als/spine_MRI required in all 30',         len(cases_with('als','order_body_imaging',[R],'spine_MRI')), 30),
    ('als/emg_ncs required in all 30',           len(cases_with('als','order_specialized_test',[R],'emg_ncs')), 30),
    ('als/respiratory_function required all 30', len(cases_with('als','order_specialized_test',[R],'respiratory_function')), 30),
    ('als/genetics recommended 26',              n_actions('als','order_specialized_test',[C],'genetic_panel'), 26),
    ('als/genetics required 4',                  n_actions('als','order_specialized_test',[R],'genetic_panel'), 4),
    ('als/no RNS, biopsy, EP, tilt', sum(n_actions('als','order_specialized_test',None,p) for p in
        ('repetitive_nerve_stimulation','muscle_biopsy','nerve_biopsy','ssep','vep','baep','tilt_table')), 0),
    ('alz/MRI required in all 30',               len(cases_with('alzheimers_early','analyze_brain_mri',[R])), 30),
    ('alz/CSF required in 13',                   len(cases_with('alzheimers_early','analyze_csf',[R])), 13),
    ('alz/CSF recommended in 17',                len(cases_with('alzheimers_early','analyze_csf',[C])), 17),
    ('alz/clinical assessment required all 30',  len(cases_with('alzheimers_early','perform_clinical_assessment',[R])), 30),
    ('alz/no case uses head CT',                 len(cases_with('alzheimers_early','order_ct_scan')), 0),
    ('nmdar/MRI required all 30',                len(cases_with('autoimmune_encephalitis_nmdar','analyze_brain_mri',[R])), 30),
    ('nmdar/EEG required all 30',                len(cases_with('autoimmune_encephalitis_nmdar','analyze_eeg',[R])), 30),
    ('nmdar/CAP CT required all 30',             len(cases_with('autoimmune_encephalitis_nmdar','order_body_imaging',[R],'chest_abdomen_pelvis_CT')), 30),
    ('men/MRI recommended in 27',                len(cases_with('bacterial_meningitis','analyze_brain_mri',[C])), 27),
    ('men/microbiology required all 30',         len(cases_with('bacterial_meningitis','order_microbiology',[R])), 30),
    ('men/no case requires ECG',                 len(cases_with('bacterial_meningitis','analyze_ecg',[R])), 0),
    ('glioma/no case requires EEG',              len(cases_with('brain_tumor_glioma','analyze_eeg',[R])), 0),
    ('glioma/perfusion_MRI in all 30',           len(cases_with('brain_tumor_glioma','order_advanced_imaging',[C],'perfusion_MRI')), 30),
    ('glioma/tissue required all 30',            len(cases_with('brain_tumor_glioma','obtain_tissue_diagnosis',[R])), 30),
    ('fepi/ECG required in 2',                   len(cases_with('focal_epilepsy_temporal','analyze_ecg',[R])), 2),
    ('fepi/no case requires EEG in ICU',         n_actions('focal_epilepsy_temporal','analyze_eeg',None,'continuous_icu'), 0),
    ('fepi/labs optional in all 30',             len(cases_with('focal_epilepsy_temporal','interpret_labs',[O])), 30),
    ('fepi/echo optional in 2, nowhere else',   (len(cases_with('focal_epilepsy_temporal','order_echocardiogram',[O])),
                                                 len(cases_with('focal_epilepsy_temporal','order_echocardiogram',[R,C]))), (2,0)),
    ('fepi/monitoring optional in 2, else none',(len(cases_with('focal_epilepsy_temporal','order_cardiac_monitoring',[O])),
                                                 len(cases_with('focal_epilepsy_temporal','order_cardiac_monitoring',[R,C]))), (2,0)),
    ('ftd/neuropsych required all 30',           len(cases_with('ftd','order_specialized_test',[R],'neuropsych_battery')), 30),
    ('ftd/genetics optional 10, recommended 7', (n_actions('ftd','order_specialized_test',[O],'genetic_panel:FTD'),
                                                 n_actions('ftd','order_specialized_test',[C],'genetic_panel:FTD')), (10,7)),
    ('ftd/clinical assessment required all 30',  len(cases_with('ftd','perform_clinical_assessment',[R])), 30),
    ('fnd/video-EEG required in 22',             len(cases_with('functional_neurological_disorder','analyze_eeg',[R])), 22),
    ('fnd/MRI optional in 23',                   len(cases_with('functional_neurological_disorder','analyze_brain_mri',[O])), 23),
    ('fnd/labs optional in 27',                  len(cases_with('functional_neurological_disorder','interpret_labs',[O])), 27),
    ('fnd/signs exam required all 30',           len(cases_with('functional_neurological_disorder','perform_clinical_assessment',[R],'functional_neuro_signs')), 30),
    ('gbs/ECG recommended all 30',               len(cases_with('guillain_barre','analyze_ecg',[C])), 30),
    ('gbs/monitoring required all 30',           len(cases_with('guillain_barre','order_cardiac_monitoring',[R])), 30),
    ('gbs/emg_ncs required all 30',              len(cases_with('guillain_barre','order_specialized_test',[R],'emg_ncs')), 30),
    ('gbs/respiratory required all 30',          len(cases_with('guillain_barre','order_specialized_test',[R],'respiratory_function')), 30),
    ('gbs/no brain MRI anywhere',                len(cases_with('guillain_barre','analyze_brain_mri')), 0),
    ('gbs/no body imaging yet (partial claim)',  len(cases_with('guillain_barre','order_body_imaging')), 0),
    ('he/brain MRI required in 5',               len(cases_with('hepatic_encephalopathy','analyze_brain_mri',[R])), 5),
    ('he/EEG recommended 23 optional 1',        (len(cases_with('hepatic_encephalopathy','analyze_eeg',[C])),
                                                 len(cases_with('hepatic_encephalopathy','analyze_eeg',[O]))), (23,1)),
    ('he/EEG never required',                    len(cases_with('hepatic_encephalopathy','analyze_eeg',[R])), 0),
    ('he/head CT required 5 recommended 0 optional 25',
        (len(cases_with('hepatic_encephalopathy','order_ct_scan',[R])),
         len(cases_with('hepatic_encephalopathy','order_ct_scan',[C])),
         len(cases_with('hepatic_encephalopathy','order_ct_scan',[O]))), (5,0,25)),
    ('he/blood culture all 30',                  len(cases_with('hepatic_encephalopathy','order_microbiology',[R],'blood_culture')), 30),
    ('he/urine all 30',                          len(cases_with('hepatic_encephalopathy','order_microbiology',[R],'urine')), 30),
    ('he/ascitic fluid in 13',                   len(cases_with('hepatic_encephalopathy','order_microbiology',[R],'ascitic_fluid')), 13),
    ('he/no body imaging yet (partial claim)',   len(cases_with('hepatic_encephalopathy','order_body_imaging')), 0),
    ('stroke/MRI optional in all 30',            len(cases_with('ischemic_stroke','analyze_brain_mri',[O])), 30),
    ('stroke/no case requires EEG',              len(cases_with('ischemic_stroke','analyze_eeg',[R])), 0),
    ('stroke/CT required in all 30',             len(cases_with('ischemic_stroke','order_ct_scan',[R])), 30),
    ('mig/MRI optional 15 recommended 5',       (len(cases_with('migraine_with_aura','analyze_brain_mri',[O])),
                                                 len(cases_with('migraine_with_aura','analyze_brain_mri',[C]))), (15,5)),
    ('mig/MRI never required',                   len(cases_with('migraine_with_aura','analyze_brain_mri',[R])), 0),
    ('mig/CSF never required nor recommended',   len(cases_with('migraine_with_aura','analyze_csf',[R,C])), 0),
    ('mig/CSF optional in exactly 1',            len(cases_with('migraine_with_aura','analyze_csf',[O])), 1),
    ('mig/EEG in exactly 1 case',                len(cases_with('migraine_with_aura','analyze_eeg')), 1),
    ('mig/labs never required',                  len(cases_with('migraine_with_aura','interpret_labs',[R])), 0),
    ('mig/ICHD-3 assessment required all 30',    len(cases_with('migraine_with_aura','perform_clinical_assessment',[R],'structured_headache_history_ichd3')), 30),
    ('mig/no ECG anywhere',                      len(cases_with('migraine_with_aura','analyze_ecg')), 0),
    ('mig/echo required in exactly 3',           len(cases_with('migraine_with_aura','order_echocardiogram',[R])), 3),
    ('ms/MRI required all 30',                   len(cases_with('multiple_sclerosis','analyze_brain_mri',[R])), 30),
    ('ms/CSF optional 29 recommended 1',        (len(cases_with('multiple_sclerosis','analyze_csf',[O])),
                                                 len(cases_with('multiple_sclerosis','analyze_csf',[C]))), (29,1)),
    ('ms/spine_MRI required all 30',             len(cases_with('multiple_sclerosis','order_body_imaging',[R],'spine_MRI')), 30),
    ('ms/OCT+VEP in all 30',                    (len(cases_with('multiple_sclerosis','order_specialized_test',None,'optical_coherence_tomography')),
                                                 len(cases_with('multiple_sclerosis','order_specialized_test',None,'vep'))), (30,30)),
    ('ms/no EEG, no ECG',                       (len(cases_with('multiple_sclerosis','analyze_eeg')),
                                                 len(cases_with('multiple_sclerosis','analyze_ecg'))), (0,0)),
    ('mg/brain MRI in exactly 1 case',           len(cases_with('myasthenia_gravis','analyze_brain_mri')), 1),
    ('mg/no CSF anywhere',                       len(cases_with('myasthenia_gravis','analyze_csf')), 0),
    ('mg/mediastinum_CT required all 30',        len(cases_with('myasthenia_gravis','order_body_imaging',[R],'mediastinum_CT')), 30),
    ('mg/RNS required in 27',                    len(cases_with('myasthenia_gravis','order_specialized_test',[R],'repetitive_nerve_stimulation')), 27),
    ('mg/SFEMG ordered in 24',                   len(cases_with('myasthenia_gravis','order_specialized_test',None,'emg_single_fiber')), 24),
    ('mg/advanced imaging required in 2',        len(cases_with('myasthenia_gravis','order_advanced_imaging',[R])), 2),
    ('nph/labs optional all 30',                 len(cases_with('nph','interpret_labs',[O])), 30),
    ('nph/advanced imaging optional all 30',     len(cases_with('nph','order_advanced_imaging',[O])), 30),
    ('nph/advanced imaging nowhere else',        len(cases_with('nph','order_advanced_imaging',[R,C])), 0),
    ('nph/neuropsych now optional all 30',       len(cases_with('nph','order_specialized_test',[O],'neuropsych_battery')), 30),
    ('nph/neuropsych no longer required',        len(cases_with('nph','order_specialized_test',[R])), 0),
    ('nph/gait assessment required all 30',      len(cases_with('nph','perform_clinical_assessment',[R],'gait_and_balance_timed')), 30),
    ('nph/MRI required all 30',                  len(cases_with('nph','analyze_brain_mri',[R])), 30),
    ('nph/CSF required all 30',                  len(cases_with('nph','analyze_csf',[R])), 30),
    ('pd/MRI required all 30',                   len(cases_with('parkinsons','analyze_brain_mri',[R])), 30),
    ('pd/labs optional all 30',                  len(cases_with('parkinsons','interpret_labs',[O])), 30),
    ('pd/no EEG, no ECG',                       (len(cases_with('parkinsons','analyze_eeg')),
                                                 len(cases_with('parkinsons','analyze_ecg'))), (0,0)),
    ('pd/no EMG, RNS, biopsy, EP', sum(n_actions('parkinsons','order_specialized_test',None,p) for p in
        ('emg_ncs','repetitive_nerve_stimulation','muscle_biopsy','nerve_biopsy','ssep','vep','baep')), 0),
    ('se/EEG required all 30',                   len(cases_with('status_epilepticus','analyze_eeg',[R])), 30),
    ('se/CT required all 30',                    len(cases_with('status_epilepticus','order_ct_scan',[R])), 30),
    ('se/MRI required in 17',                    len(cases_with('status_epilepticus','analyze_brain_mri',[R])), 17),
    ('se/no MR_venography yet (partial claim)',  n_actions('status_epilepticus','order_advanced_imaging',None,'MR_venography'), 0),
    ('sah/CSF required in 3',                    len(cases_with('subarachnoid_hemorrhage','analyze_csf',[R])), 3),
    ('sah/labs required all 30',                 len(cases_with('subarachnoid_hemorrhage','interpret_labs',[R])), 30),
    ('sah/TCD in all 30',                        len(cases_with('subarachnoid_hemorrhage','order_advanced_imaging',None,'transcranial_doppler')), 30),
    ('sah/cerebral angiography in 3',            len(cases_with('subarachnoid_hemorrhage','order_advanced_imaging',None,'cerebral_angiography')), 3),
    ('sah/CT required all 30',                   len(cases_with('subarachnoid_hemorrhage','order_ct_scan',[R])), 30),
    ('sync/ECG required all 30',                 len(cases_with('syncope_cardiac','analyze_ecg',[R])), 30),
    ('sync/no case requires EEG',                len(cases_with('syncope_cardiac','analyze_eeg',[R])), 0),
    ('sync/labs required 11 recommended 19',    (len(cases_with('syncope_cardiac','interpret_labs',[R])),
                                                 len(cases_with('syncope_cardiac','interpret_labs',[C]))), (11,19)),
    ('sync/cardiac MRI in 18',                   len(cases_with('syncope_cardiac','order_advanced_imaging',None,'cardiac_MRI')), 18),
    ('sync/monitoring required all 30',          len(cases_with('syncope_cardiac','order_cardiac_monitoring',[R])), 30),
    ('sync/echo required 29 recommended 1',     (len(cases_with('syncope_cardiac','order_echocardiogram',[R])),
                                                 len(cases_with('syncope_cardiac','order_echocardiogram',[C]))), (29,1)),
    ('sync/brain MRI required in 1',             len(cases_with('syncope_cardiac','analyze_brain_mri',[R])), 1),
]

def test_every_quantified_claim_in_the_guidance_is_true():
    fails = [f"{label}: the app says {expected}, the cases say {actual}"
             for label, actual, expected in CLAIMS if actual != expected]
    assert not fails, "\n".join(fails)


def test_the_claim_table_covers_every_condition_with_guidance():
    """A condition whose responses quote numbers but appear in no claim is unchecked."""
    import re, yaml, pathlib
    guidance = yaml.safe_load(
        pathlib.Path("agent-platform/config/review/condition_tool_guidance.yaml").read_text()
    )
    quantified = re.compile(r"all \d+ cases|no case|\d+ of (?:the )?\d+|in \d+ cases?", re.I)
    with_numbers = {
        cond for cond, tools in guidance.items()
        for entry in tools.values()
        if quantified.search(entry.get("our_response") or "")
    }
    # als/ -> als, alzheimers_early/ -> alz ... the labels are abbreviated, so match on the
    # condition appearing in any claim label prefix.
    ABBREV = {"alzheimers_early": "alz", "autoimmune_encephalitis_nmdar": "nmdar",
              "bacterial_meningitis": "men", "brain_tumor_glioma": "glioma",
              "focal_epilepsy_temporal": "fepi", "functional_neurological_disorder": "fnd",
              "guillain_barre": "gbs", "hepatic_encephalopathy": "he",
              "ischemic_stroke": "stroke", "migraine_with_aura": "mig",
              "multiple_sclerosis": "ms", "myasthenia_gravis": "mg", "parkinsons": "pd",
              "status_epilepticus": "se", "subarachnoid_hemorrhage": "sah",
              "syncope_cardiac": "sync"}
    labels = " ".join(label for label, _a, _e in CLAIMS)
    missing = sorted(
        cond for cond in with_numbers
        if f"{ABBREV.get(cond, cond)}/" not in labels
    )
    assert not missing, f"conditions whose claims are never checked: {missing}"
