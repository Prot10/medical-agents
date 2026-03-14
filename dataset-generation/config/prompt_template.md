You are an expert neurologist and medical educator creating a realistic simulated patient case for a neurology AI diagnostic benchmark called NeuroBench.

## Task

Generate a COMPLETE patient case as a single JSON object conforming EXACTLY to the schema below. Output ONLY valid JSON — no markdown fences, no commentary, no explanation before or after.

## JSON Schema

The output must conform to this exact schema:

{json_schema}

## Condition to Generate

{condition_yaml}

## Case Parameters

- **Case ID**: `{case_id}`
- **Condition**: `{condition_name}`
- **Difficulty**: `{difficulty}`
- **Encounter type**: `{encounter_type}`

## Clinical Realism Requirements

1. **Patient profile**: Create a believable patient with realistic demographics for this condition. Include a detailed, narrative-style history of present illness (at least 150 words) that reads like a real clinical encounter — not a textbook summary. Include relevant past medical history, medications with realistic doses, family history, and social history.

2. **Neurological exam**: Write a complete neurological examination with findings appropriate to the condition and difficulty level. For straightforward cases, exam findings should clearly support the diagnosis. For diagnostic puzzles, exam may be normal or subtly abnormal.

3. **Vital signs**: Use physiologically realistic values. Adjust for the clinical scenario (e.g., tachycardia in acute stroke, normal vitals in outpatient Alzheimer's).

4. **Cross-modal consistency**: ALL tool outputs must be internally consistent with each other AND with the clinical narrative. If the EEG shows right temporal findings, the MRI (if abnormal) must also show right temporal pathology. If labs are abnormal, the clinical history must explain why.

5. **Difficulty calibration**:
   - **STRAIGHTFORWARD**: Classic textbook presentation. Findings clearly point to the diagnosis. An intern should get this right.
   - **MODERATE**: Some atypical features or subtle findings. A resident would need to think carefully.
   - **DIAGNOSTIC_PUZZLE**: Misleading initial presentation. Some findings are red herrings or initially absent. Only an experienced attending would catch this early.

6. **Tool outputs**: Generate detailed, realistic tool outputs for all required modalities. Each report should read like it was written by a real specialist (radiologist, EEG technologist, lab system).

7. **Follow-up outputs**: Generate at least 5 follow-up tool outputs for predictable follow-up requests the agent might make. Each should have a clear trigger_action, tool_name, and a complete output conforming to the appropriate schema.

8. **Ground truth**: Include the correct primary diagnosis with ICD code, a ranked differential diagnosis list (at least 3 alternatives with likelihood and key features), optimal action sequence (step-by-step what the best clinician would do), critical actions (MUST do), contraindicated actions (MUST NOT do), and key reasoning points.

9. **Lab values**: Use specific numeric values with correct units and reference ranges. Mark abnormal values correctly. Include complete panels (CBC, BMP at minimum), not just cherry-picked values.

10. **Medications**: Use real drug names with realistic doses and frequencies. Include indication for each medication.

## Output Format

Output a single JSON object. No wrapping, no explanation. Just the JSON.
