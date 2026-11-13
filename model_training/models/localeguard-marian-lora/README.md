---
language:
- zh
- en
license: cc-by-4.0
base_model: Helsinki-NLP/opus-mt-zh-en
library_name: peft
pipeline_tag: translation
---
# LocaleGuard Marian LoRA

A trained Chinese-to-English translation adapter for the LocaleGuard educational localization research prototype. This is an experimental draft translator, requiring human review; it does not detect or certify cultural appropriateness.

## Attribution and artifact

Derived from [Helsinki-NLP/opus-mt-zh-en](https://huggingface.co/Helsinki-NLP/opus-mt-zh-en), by the University of Helsinki Language Technology Research Group, licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This adapter is distributed under CC BY 4.0 with attribution to the upstream model and the LocaleGuard project. Changes consist of LoRA fine-tuning on CodeCombat bilingual locale strings; no endorsement by the upstream authors is implied. Dataset attribution and MIT notice are retained in [data/codecombat](../../data/codecombat).

Base revision: `cf109095479db38d6df799875e34039d4938aaa6`.

The uploaded safetensors file contains only the adapter, not the base weights. Load it with the exact pinned base using [the prediction script](../../training/predict.py). No paid API or API key is required. See [repository instructions](../../../README.md) for setup and use.

Adapter SHA-256: `549508f99d46523dc15525f89317e35e811df7e4e4b770f4f369dc2528064532`.

## Training

- Base parameters: 77,943,296, frozen; trainable adapter parameters: 294,912.
- LoRA query/value projections, rank 8, alpha 16, dropout 0.05.
- 3,459 training pairs, 200 validation pairs, 200 held-out test pairs; grouped source/target duplicates and detected near-duplicates.
- Chinese input prefixed with its namespace category; English reference target. No invented speaker or scene context.
- Maximum input/target scope 128 tokens; seven longer examples excluded before splitting.
- Three epochs, seed 42, batch size 8, AdamW peak learning rate 0.0003, CPU.
- Epoch 3 selected by validation loss: initial 3.5135, selected 2.2350. No test-based checkpoint selection.

Full [training record](../../training_run.json), [split manifest](../../data/splits/manifest.json), and [environment lock](../../training/requirements-lock.txt) are included. Wall time includes local session gaps and is not a throughput benchmark.

## Evaluation and limitations

On the same 200 test rows, original direct translation scored BLEU 21.51 / chrF++ 44.99. The adapter scored 26.82 / 47.85. With technical checks and at most one alternate decoding attempt, LocaleGuard scored 27.11 / 47.97; two rows still had placeholder failures. Only ten source rows contain placeholders and two contain markup. See [metrics and prediction evidence](../../../evaluation/metrics.json).

These are automatic overlap scores from one split and one seed, not human ratings or statistical significance. The original base model performed worse with category prefixes; this experiment does not isolate the benefit of context. The public corpus may overlap unknown upstream pretraining data. Automatically cleaned references may still contain mistranslations; the corpus also covers account, marketing, and teacher UI, not just game dialogue. Generalization to new games, cultural judgment, and reviewer-effort savings have not been established. All generated drafts remain review-required. Human evaluation and playable-game integration remain pending.
