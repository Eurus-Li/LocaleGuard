# LocaleGuard

A small Chinese-to-English localization research prototype using CodeCombat's public bilingual locale strings. It produces translation drafts, checks technical constraints, and requires human review before export.

## About CodeCombat

[CodeCombat](https://codecombat.com/) is an educational programming game that helps learners practice coding through gameplay, using languages such as Python and JavaScript. It connects programming practice with game challenges, making it a useful setting for studying how educational content is localized for different audiences. Its [public GitHub repository](https://github.com/codecombat/codecombat) includes multilingual interface and instructional strings.

LocaleGuard uses CodeCombat's matched English and Simplified Chinese locale strings as a case study for translation, technical quality checks, and human cross-cultural review. The dataset includes game UI, programming explanations, and teacher-facing content, alongside account and marketing text. We use the public localization files; this repository does not include CodeCombat's proprietary hosted levels or a complete copy of the playable game.

## Current status

- Mirrored **6,058 original bilingual pairs** and produced **3,866 automatically cleaned unique candidates** with an exclusion log and upstream attribution.
- Completed **three epochs of local LoRA fine-tuning** of `Helsinki-NLP/opus-mt-zh-en`.
- Saved a trained **294,912-parameter adapter** on a frozen **77,943,296-parameter base model** (about 78M parameters total). The adapter weights are included in this repository; the base model downloads separately from Hugging Face.
- Evaluated the selected checkpoint on **200 held-out strings**, with reproducible splits and predictions.
- Implemented placeholder, markup, optional length/glossary checks, JSON Schema validation, one bounded retry, and an approval-gated JSONL export.
- Human quality/cultural review, review-time measurement, and playable-game integration are **not yet completed**.

This follows the midterm presentation's workflow and evaluation goals, adapted to a small local translation model instead of a hosted LLM. See [methodology and scope](docs/methodology.md) for what is implemented and what remains.

## Measured results

Same 200 test strings, one English reference each. Higher BLEU/chrF++ is better; these are automatic overlap scores, not human quality ratings.

| System | BLEU | chrF++ | Rows with technical flags |
| --- | ---: | ---: | ---: |
| Original base model, direct translation | 21.51 | 44.99 | 8 / 200 |
| Original base model, category prefix | 12.29 | 42.34 | 7 / 200 |
| Fine-tuned adapter, category prefix | 26.82 | 47.85 | 5 / 200 |
| LocaleGuard: adapter + checks + bounded retry | **27.11** | **47.97** | **2 / 200** |

The retry ran for five strings; two still had placeholder failures and remain review-required. Only ten test strings contain source placeholders and two contain markup, so technical-check results cover a small subset. No original character limits were available to score. Category prefixes hurt the unadapted base model; this comparison does not prove that adding context alone improves translation.

Checkpoint selection used validation loss only (3.5135 initially, 2.2350 at selected epoch 3). The test set was not used to select the checkpoint. This is one seed and one split, with no significance or broad generalization claim.

Detailed evidence: [metrics](evaluation/metrics.json), [training run](evaluation/training_run.json), [all test predictions](evaluation/test_predictions.jsonl), and [human-review worksheet instructions](evaluation/HUMAN_REVIEW.md). Recorded training wall time includes substantial gaps in the local session and should not be treated as a controlled throughput benchmark. No paid inference API was used; hardware/electricity costs were not measured.

## Data

| File | Purpose |
| --- | --- |
| [Original pairs](data/codecombat/original_pairs.jsonl) | Unfiltered matched source values; 6,058 rows. |
| [Cleaned data](data/codecombat/cleaned_data.jsonl) | Automatically filtered/deduplicated candidates; 3,866 rows. |
| [Cleaning documentation](data/codecombat/README.md) | Provenance, exclusion rules, license, and limitations. |
| [Split manifest](data/splits/manifest.json) | Seed, tokenizer limit, input hash, and grouping method. |
| [Training split](data/splits/train.jsonl) | 3,459 rows. |
| [Validation split](data/splits/validation.jsonl) | 200 rows for checkpoint selection. |
| [Test split](data/splits/test.jsonl) | 200 held-out rows. |

Seven cleaned examples exceed the 128-token scope and were excluded from training preparation, not removed from the original cleaned dataset. Exact source/target matches and detected near-duplicates stay in the same split. This heuristic cannot guarantee removal of all semantic overlap or overlap with the base model's pretraining data.

The corpus includes game UI, programming explanations, marketing, accounts, and teacher dashboards. It is not a scene/dialogue-only corpus. Category is the available namespace context; speaker and scene descriptions are not invented. Absence of an AI marker does not establish human authorship or correctness.

## Run the trained model

Tested with Python 3.12 and CPU on Apple Silicon. The first run requires network access to download the pinned pretrained model. Later runs can use the local cache. No API key is required.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r training/requirements.txt

python training/predict.py \
  --input examples/input.jsonl \
  --output outputs/drafts.jsonl
```

Input fields: `id`, `category`, `zh_CN`, and optional positive integer `max_chars`. Supply `--glossary path/to/glossary.json` for a reviewed Chinese-term-to-English-term map; it is used for warning checks, not forced decoding. No approved glossary is bundled.

Example observed output: `欢迎来到这个关卡。` → `Welcome to this level.` See [example predictions](examples/predictions.jsonl). Every generated record has `status: "needs_review"` and `cultural_review_required: true`, even if no technical warnings are found.

Review and edit drafts, then explicitly set `status` to `approved` and add `reviewer` and `reviewed_at`. Export rechecks the current translation and refuses unresolved technical failures:

```sh
python training/predict.py \
  --input outputs/reviewed.jsonl \
  --output outputs/approved.jsonl \
  --export-approved
```

Pass the same glossary during export if one was used for drafting. The local approval fields are a workflow convention, not authenticated sign-off. Export contains only approved IDs and translations; unapproved records are excluded.

## Reproduce the experiment

The stored splits are the authoritative split for this run. To rebuild them and retrain:

```sh
python scripts/clean_codecombat.py
python training/prepare.py
python training/train.py --epochs 3 --device cpu
python training/evaluate.py
python -m unittest discover -s tests -v
```

Training updates only query/value LoRA weights (rank 8, alpha 16, dropout 0.05), using AdamW, batch size 8, seed 42, and a 3e-4 peak learning rate. Validation loss selects the best of three epochs. A rerun overwrites generated splits, adapter weights, and evaluation files. Numerical results can vary across hardware or library versions; [the full environment lock](training/requirements-lock.txt) records the actual run.

`--base-model /path/to/local/base-model` supports an already downloaded base snapshot in prepare/train/evaluate/predict. The adapter is not a standalone model; it needs the exact base revision listed in its configuration and [model card](models/localeguard-marian-lora/README.md).

## Team and next work

**Eurus** owns data preparation, model training, and the translation pipeline. The first training run and automatic evaluation are complete; ongoing work includes supporting the reviewers and documenting subsequent model changes.

**Mike and Rong:** ownership of the two workstreams below is **TBD**. Both are open for selection; neither task has been assigned to a specific teammate.

### TODO: Cross-cultural Risk Check — owner TBD

Goal: review whether translations could cause cultural or religious misunderstanding or offense for a defined audience.

- [ ] Define the target region, cultural context, audience age, and educational setting before judging risk.
- [ ] Create a review rubric covering religious references, cultural stereotypes, identity-related wording, and age/context appropriateness, with severity levels and supporting evidence.
- [ ] Review source text and translation together; record string ID, available context, target audience, risk category, rationale, severity, and suggested revision. Mark insufficient context as needing clarification.
- [ ] Document representative cases, including acceptable expressions where relevant. A religious term alone is not evidence of risk.
- [ ] If real examples are scarce, create a separate, clearly labeled challenge set and report it separately from the real test data.

Deliverables: review rubric, annotated risk-review table, and a short case-study summary. This is a human-review workstream; its findings do not demonstrate that the model can automatically detect cultural risk.

### TODO: Model Evaluation — owner TBD

Goal: independently assess whether fine-tuning and the LocaleGuard checking/retry workflow improve translation quality.

- [ ] Read [human-review instructions](evaluation/HUMAN_REVIEW.md) and inspect the existing [automatic metrics](evaluation/metrics.json).
- [ ] Select the same sample of at least 50 held-out strings across systems and perform blind ratings using [the review worksheet](evaluation/blind_review.csv). Do not inspect [the system key](evaluation/review_key.jsonl) until ratings are complete.
- [ ] Compare the original model, fine-tuned model, and LocaleGuard workflow for accuracy, fluency, terminology consistency, and educational-context suitability; include the existing category-prefix baseline when reporting the four-system experiment.
- [ ] Audit placeholder and markup errors, including false alarms and missed errors; record review time using a consistent procedure.
- [ ] Summarize automatic scores, human ratings, remaining failures, and limitations with representative examples.

Deliverables: completed rating worksheet, error analysis, and a concise evaluation report. Preserve the current test results; if feedback is used to tune the model, use fresh held-out data for subsequent evaluation rather than repeatedly optimizing against this test set.

The two workstreams can proceed independently and be combined in the final report. Human cultural review and translation-quality evaluation remain pending. Playable-game integration is a separate future item with no owner assigned yet.

## Attribution and licenses

LocaleGuard code uses the repository's [MIT license](LICENSE). The mirrored CodeCombat locale files retain [CodeCombat's MIT notice](data/codecombat/LICENSE-CodeCombat.txt); hosted CodeCombat levels are not included or relicensed. The base translation model is by the University of Helsinki Language Technology Research Group and is distributed under CC BY 4.0. See the [model card](models/localeguard-marian-lora/README.md) for the base revision, adapter attribution, and limitations. No claim is made that the adapter is independent of its upstream model or training-data terms.
