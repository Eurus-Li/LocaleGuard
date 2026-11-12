# Human evaluation (not yet performed)

The automated run does not establish human translation quality, cultural suitability, review-time savings, or cost per accepted string.

`blind_review.csv` contains randomized system outputs with blank rating fields. Keep `review_key.jsonl` away from reviewers until scoring is finished. Reviewers can still encounter related outputs and infer system identity; this is a simple classroom review template, not a validated blind study.

For each row, rate meaning, fluency, and terminology from 1 (unusable) to 5 (correct and natural). Evaluate against the Chinese source; the English reference is one possible rendering, not the only valid answer. Mark cultural issues with an explanation grounded in the intended audience. Record elapsed review seconds, edited text, and acceptance using the same standard for every system. Do not interpret missing ratings as zero.

Have at least two bilingual reviewers assess a shared subset and resolve disagreements. Avoid using training examples. Compare review time and editing only after actual review, including inspection of flags. For false alarms, separately annotate whether each automatic warning in `test_predictions.jsonl` was warranted. The CSV deliberately hides automatic warnings for blind translation-quality scoring; effort/false-alarm review is a separate task.

Scene, speaker, and explicit UI length limits are missing from the CodeCombat locale export. Add those from verified gameplay if available; do not fabricate them. Cultural review is manual in this prototype. No claims about clinical outcomes, other languages, or emerging-economy markets follow from these results.
