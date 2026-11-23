# Cross-cultural Risk Check

**Status:** review package completed on 2026-11-23; **human cultural validation and publication approval remain pending**.

This folder contains an AI-assisted bilingual screening of the **200 real LocaleGuard test drafts**, a documented rubric, representative cases, and a separate synthetic challenge set. It does not implement or validate an automatic cultural-risk detector. No person is recorded as having approved these judgments.

## Start here

| Deliverable | Contents |
| --- | --- |
| [Review rubric](RUBRIC.md) | Audience assumptions, categories, severity, evidence, escalation and sign-off procedure |
| [Annotated review table](review_table.csv) | All 200 LocaleGuard drafts; exact source/reference/draft, rationale, proposed actions and blank human sign-off fields |
| [Case-study report](CASE_STUDIES.md) | Representative concerns, acceptable controls, counterexamples and limitations |
| [Cross-system case evidence](case_comparisons.csv) | Eight purposive IDs × four existing systems = 32 verbatim prediction records |
| [Synthetic challenge set](challenge_set.csv) | Eight invented source/candidate pairs; proposed expectations, not observed model results |
| [Machine-readable summary](summary.json) | Counts separated by decision and severity |
| [Provenance](provenance.json) | Immutable input links, Git blob SHAs and SHA-256 hashes |
| [Validation script](validate_review.py) | Standard-library consistency checks; no model download or API key |
| [Validation record](VALIDATION.md) | Passed checks, deliberate-corruption checks and verification limits |

## Scope and method

The user specified **no particular audience**. To make judgments interpretable, the analytical reference scenario is **US English, ages 13–17, a supervised programming classroom**. This is an assumption, not an established deployment market or evidence about all US learners. Parent/educator copy is assessed for adults. Junior copy retains its stated younger-learner context rather than being relabeled as teen-facing. No real school policy, learner demographics or religious community preference has been supplied.

The review reads Chinese source and English draft together, consulting the stored English reference and string namespace. References can differ from the Chinese source and are not automatic ground truth. The full screen covers only `system=localeguard`; the 32 comparison rows are selected cases, **not** a full cross-system cultural evaluation. Annotations were produced by **OpenAI Codex (AI)** in an unblinded, text-only review. The human reviewer, timestamp and decision columns are intentionally blank.

Baseline: [`f52d698`](https://github.com/Eurus-Li/LocaleGuard/tree/f52d698a92550d27463cb57f3e5780a722cad2f8). Original model outputs and test splits are unchanged. Available context is the ID and namespace, not verified game scenes, character art, speaker identity, linked pages or rendered UI.

## Descriptive triage results

| Decision | Rows | Meaning |
| --- | ---: | --- |
| `revise` | 5 | A concrete text-based concern warrants a proposed edit |
| `clarify` | 4 | Terminology, visuals or policy are needed before deciding |
| `quality_only` | 6 | Noted translation/commercial/technical issues kept separate from cultural findings |
| `no_signal` | 185 | No explicit concern identified by this screen; **not a safety or quality approval** |
| **Total real drafts** | **200** | One row per fixed test ID |

These are AI triage counts, not validated risk prevalence, detector accuracy, human agreement or an improvement score. Zero rows have human approval. The screen is not an exhaustive translation-error audit, so six `quality_only` rows must not be described as the total number of translation errors. Synthetic challenge rows are excluded from all real-data counts.

## Reproduce the checks

From the repository root, with Python 3.10+ and no extra dependencies:

```sh
python3 cultural_risk_check/validate_review.py
```

The script checks input hashes, exact coverage and text correspondence, all 32 comparison records, enums, human-sign-off boundaries, summary counts, synthetic separation and local Markdown links. It validates artifact consistency, **not the cultural correctness of AI judgments**. If upstream inputs change, retain this baseline or create a new review version rather than silently rewriting provenance.

## Human handoff and export

1. Read [RUBRIC.md](RUBRIC.md), inspect the rendered UI and resolve context questions.
2. Have a named bilingual human reviewer confirm, edit or reject each proposed judgment; escalate community-specific questions to an appropriate reviewer. Record identity, actual review timestamp and decision. Obtain content-owner approval for changes to source meaning.
3. Keep review data distinct from pipeline approval records. `review_table.csv` is not an export-ready `predict.py` input and does not grant approval.
4. Apply approved edits to the pipeline's draft JSONL, preserve placeholders/markup, rerun technical checks, and use the existing [approval-gated export workflow](../README.md#run-the-trained-model). The existing approval gate is a local convention, not authenticated sign-off.

The companion quality-evaluation workstream remains separate: no blind ratings, review-time results, new model inference or training changes were produced here. Anyone who has seen the identified systems in these case comparisons should not later claim to provide blind ratings of the same cases.
