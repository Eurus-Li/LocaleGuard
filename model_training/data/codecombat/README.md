# CodeCombat bilingual localization dataset

English and Simplified Chinese strings extracted from CodeCombat's public locale files at commit `b786f65455b90e7ea087fff7b470fb19f0ae70ad`.

## Files

| File | Records | Purpose |
| --- | ---: | --- |
| `original_pairs.jsonl` | 6,058 | All matching active string keys under `translation`, with original decoded values preserved. Includes AI markers, empty values, and duplicates. |
| `cleaned_data.jsonl` | 3,866 | Automatically filtered and deduplicated candidate translation pairs. |
| `excluded_records.jsonl` | 2,192 | One exclusion reason per removed ID; duplicate records point to the retained ID. |
| `cleaning_report.json` | | Counts by exclusion reason. |
| `source_manifest.json` | | Pinned source links, source file hashes, and the 1,040 English-only keys excluded from pairing. |
| `LICENSE-CodeCombat.txt` | | Upstream MIT license and copyright notice. |

JSONL means one JSON object per line, encoded as UTF-8. Each data row has `id`, `category`, `en`, and `zh_CN`. The ID is the full nested translation key; category is its top-level namespace. For Chinese-to-English experiments, use `zh_CN` as input and `en` as the reference. Do not expose reference text to the model during evaluation.

## Source and scope

- [English locale](https://github.com/codecombat/codecombat/blob/b786f65455b90e7ea087fff7b470fb19f0ae70ad/app/locale/en.js)
- [Simplified Chinese locale](https://github.com/codecombat/codecombat/blob/b786f65455b90e7ea087fff7b470fb19f0ae70ad/app/locale/zh-HANS.js)
- [Upstream license](https://github.com/codecombat/codecombat/blob/b786f65455b90e7ea087fff7b470fb19f0ae70ad/LICENSE)

The source contains 7,098 active English string keys and 6,058 active Chinese string keys. Pairing uses the full key, not file line positions. Comments, commented-out entries, and locale metadata outside `translation` are excluded. JavaScript escape sequences are decoded into their actual string values; JSON escaping may therefore differ from the original source notation. The source objects were parsed as data without executing repository code.

This is a mirror of the public localization pairs, not the full game or a dialogue-only corpus. It includes gameplay, educational, marketing, teacher-dashboard, and account text. Hosted game levels are not included; see [CodeCombat's separate level-content declaration](https://github.com/codecombat/codecombat/blob/b786f65455b90e7ea087fff7b470fb19f0ae70ad/LICENSE-LEVELS.md).

Copyright (c) 2015-2024 CodeCombat Inc. and other contributors. Retain the accompanying upstream license when redistributing this data.

## Cleaning rules

The first matching rule determines the exclusion reason:

1. Either value is empty after whitespace trimming: 2.
2. Either value contains `[AI_TRANSLATION]`: 1,961.
3. Either value contains a locale placeholder such as `(used in zh-HANS)`: 21.
4. English and Chinese values are identical after comparison normalization: 38.
5. Chinese value contains no character in U+3400–U+9FFF: 15.
6. English value contains no A–Z letter after comparison normalization: 5.
7. Both normalized values duplicate an earlier surviving pair: 150.

Comparison normalization strips angle-bracket spans, decodes HTML entities, collapses whitespace, and trims edges. It is deliberately used only for comparisons: stored translations retain their original text, tags, code examples, and placeholders. The first pair in upstream English key order is retained. The exclusion log preserves the IDs of subsequent duplicates. Normalization is a heuristic and can also remove angle-bracket code placeholders during comparison; inspect duplicate groups if those distinctions matter to your experiment.

The automatic filters leave 4,016 candidate records before deduplication, and 3,866 afterward. Some excluded numeric or unchanged labels may be useful for separate robustness tests.

## Reproduce cleaning

From the repository root, using Python 3 (standard library only):

```sh
python3 model_training/scripts/clean_codecombat.py
```

This reads `original_pairs.jsonl` and recreates the cleaned data, exclusions, and report. It does not modify the original pairs.

## Before training

These are candidates, not human-validated gold translations. Absence of an AI marker does not prove human authorship. Shared keys can contain regional adaptations instead of equivalent translations. Review semantic alignment and focus on relevant categories before training. The training pipeline now provides grouped train/validation/test splits in `model_training/data/splits/`; see the [split manifest](../splits/manifest.json). The original cleaned corpus remains unchanged. Preserve code tokens and placeholders; do not treat all differences as errors because some entries intentionally adapt content.
