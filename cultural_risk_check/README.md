# Cross-cultural Risk Check

Owner: **TBD — Mike or Rong**. Human review has not yet been completed. This folder is the workspace for cultural and religious risk review, independently of model-quality evaluation.

## TODO

- [ ] Define the target region, cultural context, audience age, and educational setting.
- [ ] Create a rubric for religious references, cultural stereotypes, identity-related wording, and age/context appropriateness, including severity and evidence requirements.
- [ ] Review source and translated text together. Record string ID, system/version, context, target audience, category, rationale, severity, suggested revision, and reviewer.
- [ ] Mark missing context as needing clarification; a religious reference alone does not establish risk.
- [ ] Document representative cases and proposed revisions.
- [ ] If needed, create a separate labeled challenge set; do not mix synthetic examples with real test data in reported results.

Deliverables to add here: a review rubric, annotated review table, and short case-study report. These are pending tasks, not completed results.

## Starting materials

- [Test predictions](../evaluation/test_predictions.jsonl) contain the translations to review.
- [Fixed test strings](../model_training/data/splits/test.jsonl) and [data documentation](../model_training/data/codecombat/README.md) provide IDs and available context.
- [Methodology](../model_training/docs/methodology.md) describes missing scene/speaker context and other limitations.

The existing model does not provide a validated cultural-risk detector. Human findings must not be presented as proof of automatic detection ability. Coordinate IDs and sampling with [model evaluation](../evaluation/README.md), while keeping the two review objectives distinct.
