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
    ('als/csf optional in five atypical cases',  len(cases_with('als','analyze_csf',[O])), 5),
    ('als/csf never required/recommended',       len(cases_with('als','analyze_csf',[R,C])), 0),
    ('als/spine_MRI required in all 30',         len(cases_with('als','order_body_imaging',[R],'spine_MRI')), 30),
    ('als/emg_ncs required in all 30',           len(cases_with('als','order_specialized_test',[R],'emg_ncs')), 30),
    ('als/respiratory_function recommended all 30',len(cases_with('als','order_specialized_test',[C],'respiratory_function')), 30),
    ('als/genetics optional all 30',             n_actions('als','order_specialized_test',[O],'genetic_panel'), 30),
    ('als/genetics never required/recommended',  n_actions('als','order_specialized_test',[R,C],'genetic_panel'), 0),
    ('als/no RNS, biopsy, EP, tilt', sum(n_actions('als','order_specialized_test',None,p) for p in
        ('repetitive_nerve_stimulation','muscle_biopsy','nerve_biopsy','ssep','vep','baep','tilt_table')), 0),
    ('alz/MRI required in 29',                   len(cases_with('alzheimers_early','analyze_brain_mri',[R])), 29),
    ('alz/CT alternative required in 1',         len(cases_with('alzheimers_early','order_ct_scan',[R])), 1),
    ('alz/CSF required in CJD exception',        len(cases_with('alzheimers_early','analyze_csf',[R])), 1),
    ('alz/CSF optional in 21',                   len(cases_with('alzheimers_early','analyze_csf',[O])), 21),
    ('alz/amyloid PET optional in 8',            len(cases_with('alzheimers_early','order_advanced_imaging',[O],'amyloid_PET')), 8),
    ('alz/FDG optional in 6',                    len(cases_with('alzheimers_early','order_advanced_imaging',[O],'FDG_PET')), 6),
    ('alz/perfusion SPECT optional in 1',        len(cases_with('alzheimers_early','order_advanced_imaging',[O],'perfusion_SPECT')), 1),
    ('alz/EEG optional exceptions in 2',         len(cases_with('alzheimers_early','analyze_eeg',[O])), 2),
    ('alz/genetics optional in 7',               len(cases_with('alzheimers_early','order_specialized_test',[O],'genetic_panel:early_onset_AD')), 7),
    ('alz/clinical assessment required all 30',  len(cases_with('alzheimers_early','perform_clinical_assessment',[R])), 30),
    ('nmdar/MRI required all 30',                len(cases_with('autoimmune_encephalitis_nmdar','analyze_brain_mri',[R])), 30),
    ('nmdar/routine EEG required all 30',        len(cases_with('autoimmune_encephalitis_nmdar','analyze_eeg',[R],'routine')), 30),
    ('nmdar/continuous EEG recommended 13',      len(cases_with('autoimmune_encephalitis_nmdar','analyze_eeg',[C],'continuous_icu')), 13),
    ('nmdar/female pelvic ultrasound 23',        len(cases_with('autoimmune_encephalitis_nmdar','order_body_imaging',[R],'pelvis_abdomen_ultrasound')), 23),
    ('nmdar/testicular ultrasound 4',            len(cases_with('autoimmune_encephalitis_nmdar','order_body_imaging',[R],'testicular_ultrasound')), 4),
    ('nmdar/contextual CAP CT 3',                len(cases_with('autoimmune_encephalitis_nmdar','order_body_imaging',[R],'chest_abdomen_pelvis_CT')), 3),
    ('nmdar/CSF required all 30',                len(cases_with('autoimmune_encephalitis_nmdar','analyze_csf',[R],'NMDAR_antibodies')), 30),
    ('nmdar/no FDG or blood cultures',          (len(cases_with('autoimmune_encephalitis_nmdar','order_advanced_imaging')),
                                                  len(cases_with('autoimmune_encephalitis_nmdar','order_microbiology'))), (0,0)),
    ('men/MRI required 9, recommended 1',        (len(cases_with('bacterial_meningitis','analyze_brain_mri',[R])),
                                                   len(cases_with('bacterial_meningitis','analyze_brain_mri',[C]))), (9,1)),
    ('men/microbiology required all 30',         len(cases_with('bacterial_meningitis','order_microbiology',[R])), 30),
    ('men/CSF required all 30',                  len(cases_with('bacterial_meningitis','analyze_csf',[R],'meningitis_panel')), 30),
    ('men/no case requires ECG',                 len(cases_with('bacterial_meningitis','analyze_ecg',[R])), 0),
    ('se/MR venography in pregnancy-CVST case',  len(cases_with('status_epilepticus','order_advanced_imaging',[O],'MR_venography')), 1),
    ('glioma/no case requires EEG',              len(cases_with('brain_tumor_glioma','analyze_eeg',[R])), 0),
    ('glioma/perfusion_MRI in all 30',           len(cases_with('brain_tumor_glioma','order_advanced_imaging',[C],'perfusion_MRI')), 30),
    ('glioma/tissue required all 30',            len(cases_with('brain_tumor_glioma','obtain_tissue_diagnosis',[R])), 30),
    ('fepi/ECG required in 21 first assessments',len(cases_with('focal_epilepsy_temporal','analyze_ecg',[R])), 21),
    ('fepi/continuous ICU only NCSE case',        n_actions('focal_epilepsy_temporal','analyze_eeg',None,'continuous_icu'), 1),
    ('fepi/sleep-deprived in 5',                 n_actions('focal_epilepsy_temporal','analyze_eeg',None,'sleep_deprived'), 5),
    ('fepi/ambulatory in 2',                     n_actions('focal_epilepsy_temporal','analyze_eeg',None,'ambulatory'), 2),
    ('fepi/labs optional in 23',                 len(cases_with('focal_epilepsy_temporal','interpret_labs',[O])), 23),
    ('fepi/no echo or cardiac monitoring',       (len(cases_with('focal_epilepsy_temporal','order_echocardiogram')),
                                                  len(cases_with('focal_epilepsy_temporal','order_cardiac_monitoring'))), (0,0)),
    ('fepi/chest CTA for concurrent PE',         len(cases_with('focal_epilepsy_temporal','order_body_imaging',[R],'chest_CTA')), 1),
    ('ftd/neuropsych required all 30',           len(cases_with('ftd','order_specialized_test',[R],'neuropsych_battery')), 30),
    ('ftd/genetics optional 17, none recommended/required',
        (n_actions('ftd','order_specialized_test',[O],'genetic_panel'),
         n_actions('ftd','order_specialized_test',[C,R],'genetic_panel')), (17,0)),
    ('ftd/FDG optional 29',                     n_actions('ftd','order_advanced_imaging',[O],'FDG_PET'), 29),
    ('ftd/perfusion SPECT optional 1',          n_actions('ftd','order_advanced_imaging',[O],'perfusion_SPECT'), 1),
    ('ftd/amyloid PET optional 3',              n_actions('ftd','order_advanced_imaging',[O],'amyloid_PET'), 3),
    ('ftd/no advanced required or recommended', n_actions('ftd','order_advanced_imaging',[R,C]), 0),
    ('ftd/CT used in 2',                        len(cases_with('ftd','order_ct_scan')), 2),
    ('ftd/clinical assessment required all 30',  len(cases_with('ftd','perform_clinical_assessment',[R])), 30),
    ('fnd/video-EEG optional in 22',             len(cases_with('functional_neurological_disorder','analyze_eeg',[O])), 22),
    ('fnd/MRI optional in 20',                   len(cases_with('functional_neurological_disorder','analyze_brain_mri',[O])), 20),
    ('fnd/labs optional in 12',                  len(cases_with('functional_neurological_disorder','interpret_labs',[O])), 12),
    ('fnd/no instrumental required/recommended', sum(n_actions('functional_neurological_disorder',tool,[R,C]) for tool in
        ('analyze_eeg','analyze_brain_mri','interpret_labs','analyze_csf','analyze_ecg','order_specialized_test')), 0),
    ('fnd/signs exam required all 30',           len(cases_with('functional_neurological_disorder','perform_clinical_assessment',[R],'functional_neuro_signs')), 30),
    ('gbs/ECG recommended all 30',               len(cases_with('guillain_barre','analyze_ecg',[C])), 30),
    ('gbs/monitoring required all 30',           len(cases_with('guillain_barre','order_cardiac_monitoring',[R])), 30),
    ('gbs/emg_ncs required all 30',              len(cases_with('guillain_barre','order_specialized_test',[R],'emg_ncs')), 30),
    ('gbs/respiratory required all 30',          len(cases_with('guillain_barre','order_specialized_test',[R],'respiratory_function')), 30),
    ('gbs/no brain MRI anywhere',                len(cases_with('guillain_barre','analyze_brain_mri')), 0),
    ('gbs/targeted spine MRI optional in five',  len(cases_with('guillain_barre','order_body_imaging',[O],'spine_MRI')), 5),
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
    ('he/optional post-TIPS Doppler in one',     len(cases_with('hepatic_encephalopathy','order_body_imaging',[O],'pelvis_abdomen_ultrasound')), 1),
    ('stroke/MRI optional in all 30',            len(cases_with('ischemic_stroke','analyze_brain_mri',[O])), 30),
    ('stroke/no case requires EEG',              len(cases_with('ischemic_stroke','analyze_eeg',[R])), 0),
    ('stroke/EEG optional in one mimic',         len(cases_with('ischemic_stroke','analyze_eeg',[O])), 1),
    ('stroke/CT required in all 30',             len(cases_with('ischemic_stroke','order_ct_scan',[R])), 30),
    ('stroke/two CT actions per case',           n_actions('ischemic_stroke','order_ct_scan',[R]), 60),
    ('stroke/CT perfusion optional in 2',        len(cases_with('ischemic_stroke','order_advanced_imaging',[O],'CT_perfusion')), 2),
    ('stroke/no duplicate vascular advanced',   sum(n_actions('ischemic_stroke','order_advanced_imaging',None,p) for p in
        ('MR_angiography','transcranial_doppler','carotid_duplex')), 0),
    ('mig/MRI optional 3 recommended 11',        (len(cases_with('migraine_with_aura','analyze_brain_mri',[O])),
                                                  len(cases_with('migraine_with_aura','analyze_brain_mri',[C]))), (3,11)),
    ('mig/MRI required five non-routine exceptions',len(cases_with('migraine_with_aura','analyze_brain_mri',[R])), 5),
    ('mig/CSF never required nor recommended',   len(cases_with('migraine_with_aura','analyze_csf',[R,C])), 0),
    ('mig/no CSF actions',                       len(cases_with('migraine_with_aura','analyze_csf')), 0),
    ('mig/EEG in exactly 1 case',                len(cases_with('migraine_with_aura','analyze_eeg')), 1),
    ('mig/labs never required',                  len(cases_with('migraine_with_aura','interpret_labs',[R])), 0),
    ('mig/ICHD-3 assessment required all 30',    len(cases_with('migraine_with_aura','perform_clinical_assessment',[R],'structured_headache_history_ichd3')), 30),
    ('mig/no ECG anywhere',                      len(cases_with('migraine_with_aura','analyze_ecg')), 0),
    ('mig/echo required in exactly 3',           len(cases_with('migraine_with_aura','order_echocardiogram',[R])), 3),
    ('mig/monitor required in exactly 3',        len(cases_with('migraine_with_aura','order_cardiac_monitoring',[R])), 3),
    ('ms/MRI required all 30',                   len(cases_with('multiple_sclerosis','analyze_brain_mri',[R])), 30),
    ('ms/CSF optional 19 recommended 11',       (len(cases_with('multiple_sclerosis','analyze_csf',[O])),
                                                 len(cases_with('multiple_sclerosis','analyze_csf',[C]))), (19,11)),
    ('ms/spine_MRI required all 30',             len(cases_with('multiple_sclerosis','order_body_imaging',[R],'spine_MRI')), 30),
    ('ms/OCT 8 and VEP 14, optional and targeted',(len(cases_with('multiple_sclerosis','order_specialized_test',[O],'optical_coherence_tomography')),
                                                   len(cases_with('multiple_sclerosis','order_specialized_test',[O],'vep'))), (8,14)),
    ('ms/targeted AQP4/MOG in 13',               (len(cases_with('multiple_sclerosis','interpret_labs',None,'AQP4_IgG_cell_based')),
                                                 len(cases_with('multiple_sclerosis','interpret_labs',None,'MOG_IgG_cell_based'))), (13,13)),
    ('ms/no EEG, no ECG',                       (len(cases_with('multiple_sclerosis','analyze_eeg')),
                                                 len(cases_with('multiple_sclerosis','analyze_ecg'))), (0,0)),
    ('mg/brain MRI in exactly 1 case',           len(cases_with('myasthenia_gravis','analyze_brain_mri')), 1),
    ('mg/no CSF anywhere',                       len(cases_with('myasthenia_gravis','analyze_csf')), 0),
    ('mg/mediastinum_CT required all 30',        len(cases_with('myasthenia_gravis','order_body_imaging',[R],'mediastinum_CT')), 30),
    ('mg/RNS required in 27',                    len(cases_with('myasthenia_gravis','order_specialized_test',[R],'repetitive_nerve_stimulation')), 27),
    ('mg/SFEMG ordered in 24',                   len(cases_with('myasthenia_gravis','order_specialized_test',None,'emg_single_fiber')), 24),
    ('mg/advanced imaging required in 2',        len(cases_with('myasthenia_gravis','order_advanced_imaging',[R])), 2),
    ('nph/labs optional all 30',                 len(cases_with('nph','interpret_labs',[O])), 30),
    ('nph/no advanced imaging',                  len(cases_with('nph','order_advanced_imaging')), 0),
    ('nph/no specialized tests',                 len(cases_with('nph','order_specialized_test')), 0),
    ('nph/gait assessment required all 30',      len(cases_with('nph','perform_clinical_assessment',[R],'gait_and_balance_timed')), 30),
    ('nph/MRI required all 30',                  len(cases_with('nph','analyze_brain_mri',[R])), 30),
    ('nph/CSF required all 30',                  len(cases_with('nph','analyze_csf',[R])), 30),
    ('pd/MRI required in 29',                    len(cases_with('parkinsons','analyze_brain_mri',[R])), 29),
    ('pd/CT alternative required in 1',          len(cases_with('parkinsons','order_ct_scan',[R])), 1),
    ('pd/targeted labs optional in 9',            len(cases_with('parkinsons','interpret_labs',[O])), 9),
    ('pd/no EEG, no ECG',                       (len(cases_with('parkinsons','analyze_eeg')),
                                                 len(cases_with('parkinsons','analyze_ecg'))), (0,0)),
    ('pd/no EMG, RNS, biopsy, EP', sum(n_actions('parkinsons','order_specialized_test',None,p) for p in
        ('emg_ncs','repetitive_nerve_stimulation','muscle_biopsy','nerve_biopsy','ssep','vep','baep')), 0),
    ('pd/no autonomic or tilt testing', sum(n_actions('parkinsons','order_specialized_test',None,p) for p in
        ('autonomic_testing','tilt_table')), 0),
    ('pd/neuropsych selected 11',               n_actions('parkinsons','order_specialized_test',None,'neuropsych_battery'), 11),
    ('pd/counselled genetics selected 2',       n_actions('parkinsons','order_specialized_test',None,'genetic_panel:PD'), 2),
    ('se/EEG required all 30',                   len(cases_with('status_epilepticus','analyze_eeg',[R])), 30),
    ('se/CT required all 30',                    len(cases_with('status_epilepticus','order_ct_scan',[R])), 30),
    ('se/MRI required in 17',                    len(cases_with('status_epilepticus','analyze_brain_mri',[R])), 17),
    ('sah/CSF required in 3',                    len(cases_with('subarachnoid_hemorrhage','analyze_csf',[R])), 3),
    ('sah/labs required all 30',                 len(cases_with('subarachnoid_hemorrhage','interpret_labs',[R])), 30),
    ('sah/TCD optional in all 30',               len(cases_with('subarachnoid_hemorrhage','order_advanced_imaging',[O],'transcranial_doppler')), 30),
    ('sah/cerebral angiography in 3',            len(cases_with('subarachnoid_hemorrhage','order_advanced_imaging',None,'cerebral_angiography')), 3),
    ('sah/CT required all 30',                   len(cases_with('subarachnoid_hemorrhage','order_ct_scan',[R])), 30),
    ('sah/two CT actions per case',              n_actions('subarachnoid_hemorrhage','order_ct_scan',[R]), 60),
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
