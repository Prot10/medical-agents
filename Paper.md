Analyses to do
- Test the base agent vs the fine-tuned agent on MIMIC neurology cases
- Test the base agent vs the fine-tuned agent on MIMIC cases with general conditions
- Test scaling: where does our fine-tuned model stand in skill compared with larger models that are not fine-tuned?
- Analyse each condition for significant differences and write a more clinical discussion, for example trying to understand whether a condition is less represented and also harder for physicians to diagnose
- Analyse how groups of conditions behave, acute vs chronic (on the synthetic cases; we also have them in MIMIC)
- Analyse a real deployment scenario (?)
- Show that the training works across model families, so not only Qwen but also Granite and Gemma, and smaller Qwen versions too, to see whether the effect holds at different scales
