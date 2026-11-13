# Model Evaluation

Owner: **TBD — Mike or Rong**. Automatic comparison is complete; blind human ratings, review-effort measurements, and error auditing remain pending.

## Existing results and tools

- [metrics.json](metrics.json): scores for four systems on the same 200 held-out strings.
- [test_predictions.jsonl](test_predictions.jsonl): all system predictions.
- [blind_review.csv](blind_review.csv): blank randomized human-rating worksheet.
- [HUMAN_REVIEW.md](HUMAN_REVIEW.md): rating instructions.
- [review_key.jsonl](review_key.jsonl): system identities; keep hidden from raters until scoring is complete.
- [evaluate.py](evaluate.py): reproducible automatic comparison.

Install dependencies using the [main README](../README.md), then run from the repository root:

```sh
python evaluation/evaluate.py
```

This loads the fixed test split and trained adapter from `model_training/` and writes results here. Rerunning overwrites the generated metrics, predictions, worksheet, and key; preserve completed human ratings separately before rerunning. Use `--base-model /path/to/local/base-model` for an already downloaded snapshot. This reorganization does not change the model, splits, or recorded scores.

## TODO

- [ ] Read the human-review instructions and existing automatic metrics.
- [ ] Rate the same sample of at least 50 held-out strings across systems, without consulting the system key.
- [ ] Assess accuracy, fluency, terminology consistency, and educational-context suitability.
- [ ] Compare the direct base model, category-prefix base model, fine-tuned model, and LocaleGuard checking/retry workflow.
- [ ] Audit placeholder and markup errors, false alarms, and missed errors; measure review time consistently.
- [ ] Summarize automatic and human results, representative failures, and limitations in an evaluation report.

Deliverables: completed rating worksheet, error analysis, and concise report. Preserve the original test evidence. If feedback informs tuning, use fresh held-out data for subsequent evaluation. Coordinate with [cultural risk review](../cultural_risk_check/README.md) for cultural/religious findings and [model training](../model_training/README.md) for implementation questions.
