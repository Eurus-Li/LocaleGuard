# Methodology and relationship to the midterm proposal

This implementation follows the workflow and evaluation intent of the uploaded LocaleGuard midterm presentation (slides 15–18), adapted to the team's later choice of CodeCombat data and a small local trained model. It does not claim to implement every planned final-project deliverable.

| Midterm proposal | Implemented | Limits / next work |
| --- | --- | --- |
| Chinese-to-English game text with IDs and context | Pinned CodeCombat locale pairs; source ID retained; namespace/category supplied as a prefix | The export mixes game and site text and lacks verified scene, speaker, and tone. Those are not fabricated. |
| LLM draft with context and glossary | Small pretrained Marian translation model, fine-tuned with a LoRA adapter; optional caller-provided glossary checks | This is a local sequence-to-sequence translation model, not a hosted instruction-following LLM. Glossary is checked after drafting, not forced into generation. No approved glossary was supplied. |
| Placeholders, tags, length rules; JSON Schema | Multiset checks for common placeholders; exact markup-sequence checks; explicit optional character limits; output schema | Token patterns and tag comparison are heuristic. No original length limits exist in the dataset, so the benchmark does not invent any. No semantic correctness guarantee. |
| Controlled revision loop | One retry using wider beam search when checks fail; keep the candidate with fewer flags | This is bounded alternate decoding, not a conversational model revising from textual feedback. Unresolved failures remain visible. |
| Human approval before export | All generated records need review; export requires approval, reviewer identity, review timestamp, and a fresh technical check | No interactive review UI yet. Approval fields are a local workflow convention, not authenticated sign-off. Human cultural review remains required. |
| Compare direct, context, and LocaleGuard | Same held-out strings for base-direct, base-context, fine-tuned-context, and guarded fine-tuned-context | Context prefixes are unfamiliar to the base translation model. These results do not isolate a causal context benefit. The extra raw fine-tuned condition separates retry effects. |
| Translation quality and review effort | Automated BLEU/chrF++ and technical flags; blank randomized review worksheet | Human meaning/fluency/terminology ratings, review time, editing effort, cultural judgments, and false alarms have not been collected. |
| Cost per accepted string | Local training and inference time recorded; no paid inference API | Hardware/electricity cost and accepted-string cost are unmeasured. |

## Data preparation

The original and automatically cleaned locale data remain unchanged. A second training-preparation step excludes examples exceeding 128 source or target tokenizer tokens. It never silently truncates training targets. Exact normalized Chinese or English matches are grouped, as are high-similarity candidate strings; see `model_training/data/splits/manifest.json` for thresholds. Groups are assigned to fixed train, validation, and test sets with seed 42. Related strings can still escape this heuristic. Grouping uses text only, before training; test targets are not used in model selection, glossary creation, or inference.

The fixed split is not stratified and mixes domains. The base model's OPUS pretraining data may overlap with public strings; absence of pretraining contamination has not been established. Neither these tests nor the small fine-tuning dataset establish broad cultural competence or generalization to other languages.

## Training and selection

Train LoRA adapters for attention query/value projections for three epochs. Select the checkpoint with lowest token-weighted validation cross-entropy. Evaluate the held-out test set only after selection. No hyperparameter search or test-driven checkpoint selection is performed. See `model_training/training_run.json` for actual settings and results.

## Metrics

BLEU and chrF++ are computed on complete decoded strings, including remaining tags and placeholders, against one English reference per row. They are imperfect reference-overlap measures, not human quality ratings. Report placeholder/markup errors and other flags separately. A wider-beam retry is selected by technical-flag count only, with the original retained on ties. Fewer flags need not mean a better translation. Timing includes local generation, not human review, network downloads, or full application overhead.

## References

- [Helsinki-NLP/opus-mt-zh-en model card](https://huggingface.co/Helsinki-NLP/opus-mt-zh-en)
- [Pinned base-model revision](https://huggingface.co/Helsinki-NLP/opus-mt-zh-en/tree/cf109095479db38d6df799875e34039d4938aaa6)
- [PEFT LoRA documentation](https://huggingface.co/docs/peft/main/conceptual_guides/lora)
- CodeCombat source attribution and upstream license: `model_training/data/codecombat/README.md` and `LICENSE-CodeCombat.txt`.
