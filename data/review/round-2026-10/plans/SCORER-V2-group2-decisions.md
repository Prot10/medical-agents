# Scorer v2, group 2: rejected labels and components (25 Oct 2026)

Conditions ALZ-EARLY, FTD, ISCH-STR, NMDAR-ENC, SE (150 cases). Brief:
`data/review/round-2026-10/SCORER_V2_BRIEF.md`. Only `ground_truth.diagnosis.rejected` and
`required_components` were written (through `case_io.save`). 150 cases changed, 1397 labels
(about 9 per case, mostly spelling and acronym variants of 3 to 5 competitors), components on
2 cases (SE-S05, SE-S08). Guard `test_diagnosis_labels_score_under_scorer_v2` passes for all 150;
the sanity check (primary and short labels score, each differential's own name does not) is clean
except the three noted under doubts.

## Decisions that apply to many cases

- Matching is a token set over the whole asserted answer, so a label is rejected only when its
  tokens are unlikely to occur together in a correct answer. Labels built from generic words were
  dropped for that reason: "vascular dementia"/"vascular cognitive impairment" in AD and FTD cases
  (vascular contribution is often true, and "dementia ... vascular risk" collides), "hemorrhagic
  stroke" in stroke cases ("without hemorrhagic transformation" names it; `without` is not a denial
  cue), "first-episode psychosis" and "limbic encephalitis" in NMDAR cases (both describe NMDAR
  encephalitis itself), "viral encephalitis" (collides with "post-viral").
- ALZ-EARLY: MCI-stage cases reject "dementia" (stage is the point) plus DLB/FTD/pseudodementia;
  typical AD-dementia cases reject "mild cognitive impairment", "MCI", "prodromal alzheimer",
  DLB, FTD and pseudodementia. Atypical variants (PCA, lvPPA, frontal AD, autosomal-dominant EOAD)
  get no MCI rejection: their stage is not stated and not the point.
- FTD: Alzheimer disease is rejected as "alzheimer disease", "alzheimer dementia", "early onset
  alzheimer" (not "alzheimer" or "AD" alone: "AD biomarkers negative", "autosomal dominant").
  The MND variant is rejected only where the patient has no MND; it is narrowed to "FTD-MND"
  (plus "ALS-FTD" in M02, "motor neuron disease" in S10) where a relative has ALS or a C9orf72
  expansion is found, since "ALS" may occur in a correct familial answer.
- ISCH-STR: a stroke mechanism (TOAST) the case excludes is a wrong subtype: "lacunar",
  "cardioembolic", "large artery atherosclerosis"/"atherosclerotic stroke". A mechanism that is
  partly true (mixed or multifactorial, M01, M02; undetermined, P04) is not rejected. Haemorrhage
  is rejected as "intracerebral hemorrhage"/"haemorrhage" (both spellings) only.
- NMDAR-ENC: a common set (HSV encephalitis, LGI1/CASPR2 encephalitis, primary psychiatric
  disorder, primary psychosis, schizophrenia, NMS) plus each case's own competitors. Post-HSV
  cases (P03, RP03) reject only an HSV relapse, never plain HSV encephalitis.
- SE: the scored diagnosis is the SE; the etiology is not made a component (it is credited by
  the action criteria), except where the label names two concurrent entities (SE-S05 Wernicke
  encephalopathy, SE-S08 eclampsia plus breakthrough epilepsy). NCSE vs convulsive subtype is not
  rejected anywhere (they coexist and evolve into each other).

## Per case

- ALZ-EARLY-M01: rejected dementia; DLB; FTD; bvFTD; FTLD; pseudodementia
- ALZ-EARLY-M02: rejected dementia; DLB; FTD; bvFTD; FTLD; pseudodementia
- ALZ-EARLY-M03: rejected dementia; DLB; FTD; bvFTD; FTLD; pseudodementia
- ALZ-EARLY-M04: rejected dementia; DLB; FTD; bvFTD; FTLD; pseudodementia
- ALZ-EARLY-M05: rejected mild cognitive impairment; MCI; prodromal alzheimer; dementia with lewy bodies; lewy body dementia; DLB; frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; pseudodementia
- ALZ-EARLY-P01: rejected corticobasal syndrome; corticobasal degeneration; CBS; dementia with lewy bodies; lewy body dementia; DLB; creutzfeldt-jakob disease; CJD; sCJD
- ALZ-EARLY-P02: rejected semantic variant primary progressive aphasia; svPPA; semantic dementia; nfvPPA; nonfluent agrammatic; agrammatic variant; progressive nonfluent aphasia; PNFA; frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration
- ALZ-EARLY-P03: rejected frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; corticobasal syndrome; corticobasal degeneration; CBS; progressive supranuclear palsy; PSP; primary psychiatric disorder
- ALZ-EARLY-P04: rejected frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; sporadic alzheimer; autoimmune encephalitis; limbic encephalitis; CADASIL; prion disease
- ALZ-EARLY-RM01: rejected mild cognitive impairment; MCI; prodromal alzheimer; dementia with lewy bodies; lewy body dementia; DLB; frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; pseudodementia
- ALZ-EARLY-RM02: rejected mild cognitive impairment; MCI; prodromal alzheimer; dementia with lewy bodies; lewy body dementia; DLB; frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; pseudodementia; normal pressure hydrocephalus; NPH
- ALZ-EARLY-RM03: rejected mild cognitive impairment; MCI; prodromal alzheimer; dementia with lewy bodies; lewy body dementia; DLB; frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; pseudodementia
- ALZ-EARLY-RM04: rejected dementia; DLB; FTD; bvFTD; FTLD; pseudodementia; lvPPA; logopenic variant; primary progressive aphasia
- ALZ-EARLY-RP01: rejected corticobasal syndrome; corticobasal degeneration; CBS; dementia with lewy bodies; lewy body dementia; DLB; creutzfeldt-jakob disease; CJD; sCJD; brain metastasis; chemotherapy-related cognitive impairment
- ALZ-EARLY-RP02: rejected corticobasal syndrome; corticobasal degeneration; CBS; dementia with lewy bodies; lewy body dementia; DLB; creutzfeldt-jakob disease; CJD; sCJD
- ALZ-EARLY-RP03: rejected corticobasal syndrome; corticobasal degeneration; CBS; dementia with lewy bodies; lewy body dementia; DLB; creutzfeldt-jakob disease; CJD; sCJD
- ALZ-EARLY-RP04: rejected mild cognitive impairment; MCI; prodromal alzheimer; creutzfeldt-jakob disease; CJD; sCJD; prion disease; autoimmune encephalitis; limbic encephalitis; paraneoplastic; frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; pseudodementia
- ALZ-EARLY-RP05: rejected mild cognitive impairment; MCI; prodromal alzheimer; dementia with lewy bodies; lewy body dementia; DLB; frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; pseudodementia; parkinson disease dementia; PDD; epilepsy | epilepsy rejected: the EEG and key evidence make epilepsy unlikely; B12 deficiency is a true contributor, not rejected
- ALZ-EARLY-RS01: rejected mild cognitive impairment; MCI; prodromal alzheimer; dementia with lewy bodies; lewy body dementia; DLB; frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; pseudodementia
- ALZ-EARLY-RS02: rejected mild cognitive impairment; MCI; prodromal alzheimer; dementia with lewy bodies; lewy body dementia; DLB; frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; pseudodementia; normal pressure hydrocephalus; NPH
- ALZ-EARLY-RS03: rejected mild cognitive impairment; MCI; prodromal alzheimer; dementia with lewy bodies; lewy body dementia; DLB; frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; pseudodementia
- ALZ-EARLY-RS04: rejected mild cognitive impairment; MCI; prodromal alzheimer; dementia with lewy bodies; lewy body dementia; DLB; frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; pseudodementia
- ALZ-EARLY-RS05: rejected mild cognitive impairment; MCI; prodromal alzheimer; dementia with lewy bodies; lewy body dementia; DLB; frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; pseudodementia
- ALZ-EARLY-RS06: rejected mild cognitive impairment; MCI; prodromal alzheimer; dementia with lewy bodies; lewy body dementia; DLB; frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; pseudodementia
- ALZ-EARLY-S01: rejected mild cognitive impairment; MCI; prodromal alzheimer; dementia with lewy bodies; lewy body dementia; DLB; frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; pseudodementia
- ALZ-EARLY-S02: rejected mild cognitive impairment; MCI; prodromal alzheimer; dementia with lewy bodies; lewy body dementia; DLB; frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; pseudodementia
- ALZ-EARLY-S03: rejected mild cognitive impairment; MCI; prodromal alzheimer; dementia with lewy bodies; lewy body dementia; DLB; frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; pseudodementia
- ALZ-EARLY-S04: rejected mild cognitive impairment; MCI; prodromal alzheimer; dementia with lewy bodies; lewy body dementia; DLB; frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; pseudodementia
- ALZ-EARLY-S05: rejected mild cognitive impairment; MCI; prodromal alzheimer; dementia with lewy bodies; lewy body dementia; DLB; frontotemporal dementia; FTD; bvFTD; FTLD; frontotemporal lobar degeneration; pseudodementia
- ALZ-EARLY-S06: rejected dementia; DLB; FTD; bvFTD; FTLD; pseudodementia; vascular cognitive impairment
- FTD-M01: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; pseudodementia
- FTD-M02: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; FTD-MND; ALS-FTD; primary psychiatric disorder | MND variant narrowed to FTD-MND / ALS-FTD: the brother died of ALS, so plain ALS/MND words may occur in a correct familial answer
- FTD-M03: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; korsakoff; wernicke; alcohol-related brain damage; normal pressure hydrocephalus; NPH
- FTD-M04: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; hashimoto encephalopathy; SREAT; primary psychiatric disorder
- FTD-M05: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; lithium toxicity; lithium neurotoxicity | bipolar disorder is a true comorbidity, not rejected
- FTD-M06: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; progressive supranuclear palsy; PSP | CBS features are true here, not rejected
- FTD-M07: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; wernicke; korsakoff; mania | alcohol-related damage is a true comorbidity; only Wernicke-Korsakoff and mania rejected
- FTD-M08: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; HIV-associated neurocognitive disorder; HAND; HIV-associated dementia; PML; progressive multifocal leukoencephalopathy; cryptococcal; toxoplasmosis
- FTD-M09: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; mania; delirium; autoimmune encephalitis
- FTD-M10: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; semantic variant primary progressive aphasia; svPPA; semantic dementia; pseudodementia
- FTD-P01: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; hyperammonemic encephalopathy; hyperammonaemic encephalopathy
- FTD-P02: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; schizophrenia; autoimmune encephalitis | primary psychiatric disorder not rejected: the label says the patient was misdiagnosed as psychiatric, so a correct answer may name it
- FTD-P03: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; pseudodementia; progressive supranuclear palsy; PSP; corticobasal syndrome; corticobasal degeneration; CBS; autoimmune encephalitis; rheumatoid meningitis; vasculitis; leukoencephalopathy
- FTD-P04: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; PD dementia; PDD; dementia with lewy bodies; lewy body dementia; DLB; progressive supranuclear palsy; PSP; wilson disease | PD is a true comorbidity: only PD dementia/PDD rejected; dopaminergic ICD not rejected (impulsivity on levodopa is real)
- FTD-P05: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; phenocopy; autoimmune encephalitis; primary psychiatric disorder
- FTD-P06: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; normal pressure hydrocephalus; NPH
- FTD-P07: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; phenocopy; pseudodementia; FTD-MND; FTD-ALS; ALS-FTD; motor neuron disease; motor neurone disease; amyotrophic lateral sclerosis
- FTD-P08: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; ALSci; ALSbi; ALScbi; benign fasciculation syndrome; cervical spondylotic myelopathy; cervical spondylotic myeloradiculopathy; progressive supranuclear palsy; PSP
- FTD-S01: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; primary psychiatric disorder; alcohol-related brain damage; alcohol-related dementia; korsakoff; wernicke; progressive supranuclear palsy; PSP; corticobasal syndrome; corticobasal degeneration; CBS; normal pressure hydrocephalus; NPH; FTD-MND; FTD-ALS; ALS-FTD; motor neuron disease; motor neurone disease; amyotrophic lateral sclerosis
- FTD-S02: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; primary psychiatric disorder; FTD-MND; FTD-ALS; ALS-FTD; motor neuron disease; motor neurone disease; amyotrophic lateral sclerosis
- FTD-S03: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; primary psychiatric disorder; FTD-MND; FTD-ALS; ALS-FTD; motor neuron disease; motor neurone disease; amyotrophic lateral sclerosis
- FTD-S04: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; primary psychiatric disorder; progressive supranuclear palsy; PSP; corticobasal syndrome; corticobasal degeneration; CBS; normal pressure hydrocephalus; NPH; FTD-MND; FTD-ALS; ALS-FTD; motor neuron disease; motor neurone disease; amyotrophic lateral sclerosis
- FTD-S05: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; obsessive-compulsive disorder; alcohol-related brain damage; alcohol-related dementia; korsakoff; FTD-MND; FTD-ALS; ALS-FTD; motor neuron disease; motor neurone disease; amyotrophic lateral sclerosis
- FTD-S06: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; alcohol-related brain damage; alcohol-related dementia; korsakoff; chronic traumatic encephalopathy; post-traumatic stress disorder
- FTD-S07: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; corticobasal syndrome; corticobasal degeneration; CBS
- FTD-S08: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; FTD-MND; FTD-ALS; ALS-FTD; motor neuron disease; motor neurone disease; amyotrophic lateral sclerosis
- FTD-S09: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; alcohol-related brain damage; alcohol-related dementia; korsakoff; normal pressure hydrocephalus; NPH
- FTD-S10: rejected alzheimer disease; alzheimer dementia; early onset alzheimer; FTD-MND; motor neuron disease; motor neurone disease; alcohol-related brain damage; alcohol-related dementia; korsakoff; huntington disease | MND variant narrowed to FTD-MND / motor neuron disease: C9orf72 expansion, so 'FTD-ALS spectrum' may occur in a correct answer
- FTD-S11: rejected alzheimer disease; alzheimer dementia; bvFTD; behavioral variant frontotemporal dementia; behavioural variant frontotemporal dementia; nfvPPA; nonfluent agrammatic; agrammatic variant; lvPPA; logopenic; herpes simplex encephalitis; HSV encephalitis; herpes encephalitis
- FTD-S12: rejected progressive supranuclear palsy; PSP; corticobasal syndrome; corticobasal degeneration; CBS; alzheimer disease; lvPPA; logopenic; semantic variant primary progressive aphasia; svPPA; semantic dementia; ischemic stroke; ischaemic stroke
- ISCH-STR-M01: rejected lacunar; intracerebral hemorrhage; intracerebral haemorrhage | mixed LAA + AF mechanism: neither mechanism rejected; no components (one disease, two mechanisms)
- ISCH-STR-M02: rejected intracerebral hemorrhage; intracerebral haemorrhage | multifactorial mechanism: every mechanism in the differential is partly true, none rejected
- ISCH-STR-M03: rejected lacunar; large artery atherosclerosis; atherosclerotic stroke; intracerebral hemorrhage; intracerebral haemorrhage
- ISCH-STR-M04: rejected vestibular neuritis; BPPV; multiple sclerosis; demyelinating; large artery atherosclerosis; atherosclerotic; posterior fossa hemorrhage; posterior fossa haemorrhage
- ISCH-STR-M05: rejected cardioembolic; lacunar; artery to artery embolism; functional neurological disorder; todd paralysis; todd paresis; intracerebral hemorrhage; intracerebral haemorrhage
- ISCH-STR-P01: rejected vestibular neuritis; BPPV; cerebellar hemorrhage; cerebellar haemorrhage; migraine with brainstem aura; multiple sclerosis; paradoxical embolism
- ISCH-STR-P02: rejected moyamoya syndrome; arterial dissection; artery dissection; vasculitis; primary angiitis; hemiplegic migraine; multiple sclerosis
- ISCH-STR-P03: rejected mycotic aneurysm; brain abscess; meningitis; marantic endocarditis; nonbacterial thrombotic endocarditis; atrial fibrillation; paradoxical embolism; vasculitis; intracerebral hemorrhage; intracerebral haemorrhage
- ISCH-STR-P04: rejected stroke mimic; cryptogenic; todd paralysis; todd paresis; intracerebral hemorrhage; intracerebral haemorrhage | mechanism not settled in the label (CE vs LAA), so neither rejected; cryptogenic rejected as the work-up names a mechanism candidate
- ISCH-STR-P05: rejected migrainous infarction; atrial fibrillation; antiphospholipid; arterial dissection; artery dissection; vasculitis; large artery atherosclerosis
- ISCH-STR-RM01: rejected cardioembolic; hemiplegic migraine; functional neurological disorder; multiple sclerosis; todd paralysis; todd paresis
- ISCH-STR-RM02: rejected trigeminal neuralgia; giant cell arteritis; temporal arteritis; acute coronary syndrome; temporomandibular; ischemic stroke; ischaemic stroke; cerebral infarction; TIA | no completed infarct: ischemic stroke/TIA rejected (the label's own 'cerebral infarct' cannot be, it names it)
- ISCH-STR-RM03: rejected cluster headache; subarachnoid hemorrhage; subarachnoid haemorrhage; tolosa-hunt; carotid-cavernous fistula; pancoast; ischemic stroke; ischaemic stroke; cerebral infarction; TIA
- ISCH-STR-RM04: rejected subarachnoid hemorrhage; subarachnoid haemorrhage; SAH; cerebellar hemorrhage; cerebellar haemorrhage; cardioembolic; large artery atherosclerosis; atherosclerotic; vestibular neuritis; basilar artery occlusion
- ISCH-STR-RP01: rejected wernicke; hepatic encephalopathy; toxic encephalopathy; brainstem hemorrhage; brainstem haemorrhage; cerebellar hemorrhage; cerebellar haemorrhage; vertebral artery dissection | alcohol intoxication cannot be rejected: the primary label names it ('misattributed to alcohol intoxication'); vertebral dissection rejected: CTA shows none
- ISCH-STR-RP02: rejected TTP relapse; relapsed TTP; cerebral venous sinus thrombosis; cerebral venous thrombosis; CVST; RCVS; reversible cerebral vasoconstriction; PRES; posterior reversible encephalopathy; cardioembolic; antiphospholipid
- ISCH-STR-RP03: rejected arterial dissection; artery dissection; cerebral venous thrombosis; cerebral venous sinus thrombosis; VITT; vaccine induced; antiphospholipid; vasculitis; atrial fibrillation
- ISCH-STR-RP04: rejected complicated migraine; hemiplegic migraine; arterial dissection; artery dissection; libman-sacks; atrial fibrillation; paradoxical embolism; vasculitis; todd paralysis; todd paresis
- ISCH-STR-RP05: rejected hypertensive small vessel disease; cardioembolic; large artery atherosclerosis; MELAS; multiple sclerosis
- ISCH-STR-RS01: rejected large artery atherosclerosis; atherosclerotic stroke; intracerebral hemorrhage; intracerebral haemorrhage | lacunar not rejected: an old right basal ganglia lacunar infarct is on record
- ISCH-STR-RS02: rejected cardioembolic; septic embolism; watershed; hypoperfusion; intracerebral hemorrhage; intracerebral haemorrhage
- ISCH-STR-RS03: rejected large artery atherosclerosis; atherosclerotic stroke; trousseau; nonbacterial thrombotic endocarditis; marantic; brain metastasis; septic embolism; air embolism
- ISCH-STR-RS04: rejected cerebral venous sinus thrombosis; cerebral venous thrombosis; CVST; vertebral artery dissection; cardioembolic; peripartum cardiomyopathy; antiphospholipid; PRES; eclampsia | paradoxical embolism not rejected: the echo leaves PFO open (saline study recommended)
- ISCH-STR-RS05: rejected cardioembolic; brain tumor; brain tumour; intracerebral hemorrhage; intracerebral haemorrhage
- ISCH-STR-S01: rejected lacunar; large artery atherosclerosis; atherosclerotic stroke; intracerebral hemorrhage; intracerebral haemorrhage
- ISCH-STR-S02: rejected lacunar; large artery atherosclerosis; atherosclerotic stroke; intracerebral hemorrhage; intracerebral haemorrhage; PRES; posterior reversible encephalopathy
- ISCH-STR-S03: rejected lacunar; large artery atherosclerosis; atherosclerotic stroke; intracerebral hemorrhage; intracerebral haemorrhage; LV thrombus; left ventricular thrombus | LV thrombus rejected: the echo shows none
- ISCH-STR-S04: rejected lacunar; large artery atherosclerosis; atherosclerotic stroke; intracerebral hemorrhage; intracerebral haemorrhage
- ISCH-STR-S05: rejected lacunar; large artery atherosclerosis; atherosclerotic stroke; intracerebral hemorrhage; intracerebral haemorrhage; todd paralysis; todd paresis
- ISCH-STR-S06: rejected cardioembolic; large artery atherosclerosis; atherosclerotic stroke; large vessel; capsular warning syndrome; multiple sclerosis; demyelinating; intracerebral hemorrhage; intracerebral haemorrhage
- NMDAR-ENC-M01: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS; neuropsychiatric lupus; NPSLE; lupus cerebritis; hyponatremic encephalopathy; hyponatraemic encephalopathy; serotonin syndrome
- NMDAR-ENC-M02: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS; neuropsychiatric lupus; NPSLE; lupus cerebritis; serotonin syndrome
- NMDAR-ENC-M03: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS; neuropsychiatric lupus; NPSLE; lupus cerebritis
- NMDAR-ENC-M04: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS
- NMDAR-ENC-M05: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS; psychotic depression; serotonin syndrome
- NMDAR-ENC-P01: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS; neuropsychiatric lupus; NPSLE; lupus cerebritis
- NMDAR-ENC-P02: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS
- NMDAR-ENC-P03: rejected HSV encephalitis relapse; herpes simplex encephalitis relapse; recurrent HSV encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS | post-HSV case: plain HSV encephalitis labels not rejected (the true label names HSV); only an HSV relapse
- NMDAR-ENC-P04: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS
- NMDAR-ENC-P05: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS
- NMDAR-ENC-P06: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS; confusional migraine
- NMDAR-ENC-P07: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS; neuropsychiatric lupus; NPSLE; lupus cerebritis; cannabis-induced psychosis
- NMDAR-ENC-P08: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS; hashimoto encephalopathy; SREAT
- NMDAR-ENC-RM01: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS; hashimoto encephalopathy; SREAT
- NMDAR-ENC-RM02: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS; hashimoto encephalopathy; SREAT; ADEM; acute disseminated encephalomyelitis; MOGAD; NMOSD; primary angiitis; CNS vasculitis
- NMDAR-ENC-RM03: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; anti-Hu; CRMP5; paraneoplastic limbic encephalitis; creutzfeldt-jakob disease; CJD; sCJD; alzheimer disease; pseudodementia; hyponatraemic encephalopathy; hyponatremic encephalopathy; serotonin syndrome
- NMDAR-ENC-RP01: rejected SARS-CoV-2 encephalitis; COVID-19 encephalopathy; herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; creutzfeldt-jakob disease; CJD; sCJD; LGI1 encephalitis; CASPR2 encephalitis; IgLON5; ischemic stroke; ischaemic stroke; osmotic demyelination; NCSE; non-convulsive status epilepticus
- NMDAR-ENC-RP02: rejected NCSE; non-convulsive status epilepticus; herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; leptomeningeal carcinomatosis; brain metastases; anti-Hu; anti-Ma2; creutzfeldt-jakob disease; CJD; sCJD; toxic metabolic encephalopathy
- NMDAR-ENC-RP03: rejected HSV encephalitis relapse; herpes simplex encephalitis relapse; recurrent HSV encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; creutzfeldt-jakob disease; CJD; sCJD; neuroleptic malignant syndrome; NMS; serotonin syndrome; levetiracetam induced; levetiracetam related
- NMDAR-ENC-RS01: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS; neuropsychiatric lupus; NPSLE; lupus cerebritis
- NMDAR-ENC-RS02: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; ADEM; acute disseminated encephalomyelitis; MOGAD; NMOSD; wernicke; hyperammonemic encephalopathy; hyperammonaemic encephalopathy; valproate encephalopathy; creutzfeldt-jakob disease; CJD; sCJD; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS
- NMDAR-ENC-RS03: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; HHV-7 encephalitis; tick-borne encephalitis; lyme; neuroborreliosis; LGI1 encephalitis; CASPR2 encephalitis; neuroleptic malignant syndrome; NMS | HHV-7 encephalitis rejected: HHV-7 PCR positive is the red herring of uncertain significance
- NMDAR-ENC-RS04: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; MOGAD; NMOSD; tuberculous meningitis; cryptococcal meningitis; neurosyphilis; LGI1 encephalitis; CASPR2 encephalitis; neuropsychiatric lupus; NPSLE; lupus cerebritis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS
- NMDAR-ENC-S01: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS; bacterial meningitis; bacterial meningoencephalitis
- NMDAR-ENC-S02: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS; neuropsychiatric lupus; NPSLE; lupus cerebritis
- NMDAR-ENC-S03: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS; neuropsychiatric lupus; NPSLE; lupus cerebritis
- NMDAR-ENC-S04: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS; neuropsychiatric lupus; NPSLE; lupus cerebritis
- NMDAR-ENC-S06: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS
- NMDAR-ENC-S09: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS
- NMDAR-ENC-S10: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; LGI1 encephalitis; CASPR2 encephalitis; primary psychiatric disorder; primary psychosis; schizophrenia; neuroleptic malignant syndrome; NMS; postpartum psychosis; hashimoto encephalopathy; SREAT
- SE-M01: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; anti-NMDAR encephalitis; LGI1; PNES; psychogenic non-epileptic seizures; functional seizures; psychogenic; acute ischemic stroke; acute ischaemic stroke
- SE-M02: rejected intratumoral hemorrhage; intratumoral haemorrhage
- SE-M03: rejected neuropsychiatric lupus; NPSLE; lupus cerebritis; CNS lupus; autoimmune encephalitis
- SE-M04: rejected recurrent stroke; new stroke; subdural hematoma; subdural haematoma; uremic encephalopathy; uraemic encephalopathy | carbamazepine toxicity (moderate, level 14.2) not rejected: the level is supratherapeutic, so it may be named truthfully
- SE-M05: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; bacterial meningitis; LGI1; anti-Hu; anti-Ma2; serotonin syndrome; primary psychiatric disorder
- SE-M06: rejected anti-NMDAR encephalitis; autoimmune encephalitis; LGI1; VZV encephalitis; enterovirus; brain abscess; aseptic meningitis; bacterial meningitis
- SE-M07: rejected lance-adams syndrome; convulsive syncope; leukoencephalopathy; toxic metabolic encephalopathy
- SE-M08: rejected primary CNS lymphoma; PCNSL; lymphoma; brain abscess; tuberculoma; cryptococcal meningitis; PML; progressive multifocal leukoencephalopathy
- SE-M09: rejected acute ischemic stroke; acute ischaemic stroke; alzheimer disease; septic encephalopathy; sepsis-associated encephalopathy
- SE-P01: rejected herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; anti-NMDAR encephalitis; LGI1; alcohol withdrawal; delirium tremens; wernicke; hepatic encephalopathy
- SE-P02: rejected status epilepticus; GCSE; frontal lobe seizures; hypermotor seizures; autoimmune encephalitis; hemiplegic migraine | status epilepticus is the designed mimic; risk: 'PNES mimicking status epilepticus' phrasing is also rejected
- SE-P03: rejected lance-adams syndrome; septic encephalopathy; sepsis-associated encephalopathy
- SE-P04: rejected status epilepticus; NCSE; hemorrhagic transformation; haemorrhagic transformation; hyperperfusion syndrome; PRES; todd paralysis; todd paresis | LPDs on the ictal-interictal continuum without SE: NCSE/SE is the designed competitor
- SE-P05: rejected carbamate; nerve agent; anticholinergic toxidrome; sympathomimetic toxidrome; septic shock
- SE-P06: rejected autoimmune encephalitis; LGI1; herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; variant CJD; vCJD; familial CJD; genetic prion disease; toxic metabolic encephalopathy
- SE-P07: rejected NCSE; wernicke; subdural hematoma; subdural haematoma; bacterial meningitis; uremic encephalopathy; uraemic encephalopathy | only 'NCSE' rejectable: the primary label itself names 'non-convulsive status epilepticus' (after 'mimicking')
- SE-P08: rejected NORSE; bacterial meningitis; herpes simplex encephalitis; HSV encephalitis; herpes encephalitis; gyromitra; salicylate; toxic alcohol; sepsis
- SE-RS11: rejected PNES; psychogenic non-epileptic seizures; functional seizures; psychogenic; alcohol withdrawal; meningitis; encephalitis
- SE-S01: rejected PNES; psychogenic non-epileptic seizures; functional seizures; psychogenic; alcohol withdrawal; meningitis; encephalitis
- SE-S02: rejected GAD65; LGI1; meningitis; encephalitis
- SE-S03: rejected recurrent stroke; new stroke; subdural hematoma; subdural haematoma; meningitis; encephalitis
- SE-S04: rejected neuropsychiatric lupus; NPSLE; lupus cerebritis; PRES; posterior reversible encephalopathy; meningitis; encephalitis
- SE-S05: rejected hepatic encephalopathy; subdural hematoma; subdural haematoma; traumatic intracranial hemorrhage; traumatic intracranial haemorrhage; meningitis; encephalitis | components [wernicke / thiamine deficiency] | component: concurrent Wernicke encephalopathy must be named with the SE; hypoglycaemia not rejected (glucose 54)
- SE-S06: rejected exertional heat stroke; methamphetamine; cocaine; neuroleptic malignant syndrome; NMS; meningitis; encephalitis; idiopathic generalized epilepsy
- SE-S07: rejected intratumoral hemorrhage; intratumoral haemorrhage; acute ischemic stroke; acute ischaemic stroke; meningitis; encephalitis
- SE-S08: rejected TTP; thrombotic thrombocytopenic purpura; cerebral venous sinus thrombosis; cerebral venous thrombosis; CVST; ischemic stroke; ischaemic stroke; intracerebral hemorrhage; intracerebral haemorrhage | components [eclampsia / eclamptic] + [epilepsy / lamotrigine] | components: concurrent eclampsia and breakthrough epilepsy, the case's designed pair ('eclampsia alone' is a moderate differential)
- SE-S09: rejected meningitis; subtherapeutic; nonadherence | subtherapeutic/non-adherence rejected: the level is toxic, the opposite mechanism
- SE-S10: rejected diphenhydramine; cocaine; meningitis; encephalitis
- SE-S11: rejected subdural hematoma; subdural haematoma; PRES; hypertensive encephalopathy; septic encephalopathy
- SE-S12: rejected PNES; psychogenic non-epileptic seizures; functional seizures; psychogenic; functional movement disorder; anti-NMDAR; NMDAR encephalitis; herpes simplex encephalitis; HSV encephalitis; herpes encephalitis

## Doubts for the physicians

1. SE etiology: should encephalitis- or tumour-headed SE cases (SE-M05 NMDAR encephalitis, SE-M06
   HSV encephalitis, SE-M08 CNS toxoplasmosis, SE-P01 anti-Hu limbic encephalitis, and by the same
   logic SE-M01, SE-M02, SE-S07) require the underlying disease as a component? Today "status
   epilepticus" alone scores in all of them. Likewise SE-S06 (serotonin syndrome), SE-S10 (TCA
   plus MDMA) and SE-S04 (valproate hyperammonaemia), whose differentials contrast "X alone".
2. SE-S08 components require eclampsia and epilepsy (or lamotrigine): "eclamptic status
   epilepticus" alone now fails. Confirm that naming the breakthrough epilepsy is required.
3. SE-P07: the primary label names "non-convulsive status epilepticus" (after "mimicking"), so
   only "NCSE" could be rejected; a hedge "HE vs non-convulsive status epilepticus" still scores.
   Suggest rewording the label (e.g. "... triphasic waves; NCSE excluded").
4. SE-P02: "status epilepticus" is rejected (the designed mimic), which also rejects a correct
   answer phrased "PNES mimicking status epilepticus". Same pattern for "NCSE" in SE-P04.
5. FTD-P08, SE-M09: differentials "ALS ... without frontotemporal dementia" and "UTI delirium
   without SE" score because `without` is not a denial cue in `_affirmed`. Suggest adding
   "without" (and "negative", "absent") to the denial cues in the scorer.
6. Typical AD-dementia cases reject "mild cognitive impairment": an answer written "mild dementia
   ... multidomain cognitive impairment" contains those three words and would fail.
7. NMDAR-ENC-RS03 rejects "HHV-7 encephalitis" (HHV-7 PCR positive is the red herring): an
   answer "anti-NMDAR encephalitis, possibly HHV-7 triggered" would fail. Confirm.
8. LGI1/CASPR2 rejections fail an answer that lists negative antibodies ("LGI1 negative"), since
   "negative" is not a denial cue.

## Class rules for the synonym YAML (not edited)

- Per ICD G41.x (SE) cases: PNES labels as rejected wherever PNES is in the differential.
- G31.09 (bvFTD): "alzheimer disease", "alzheimer dementia", "early onset alzheimer" rejected by
  default; F/G30 (AD dementia) codes: "mild cognitive impairment", "MCI", "prodromal alzheimer"
  rejected; G31.84 (MCI): "dementia" rejected.
- G04.81 NMDAR: HSV encephalitis labels rejected unless the case is post-HSV.
- I63.x with a stated TOAST mechanism: the other mechanisms ("lacunar", "cardioembolic", "large
  artery atherosclerosis") rejected.

## Lead follow-up (25 Oct 2026)
- The scorer now drops "mimicking X", "misdiagnosed as X", "without X" and "X negative" from the
  asserted text, so SE-P07 also rejects "non-convulsive status epilepticus" and "status
  epilepticus" (its primary label's "mimicking non-convulsive status epilepticus" no longer
  names them), SE-P02's "PNES mimicking SE" scores, and "LGI1-negative" answers pass.
