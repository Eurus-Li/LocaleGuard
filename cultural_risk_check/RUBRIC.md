# Cultural review rubric

Version 1 · 2026-11-23 · project-specific editorial procedure · human validation pending.

## Audience and evidence rules

Use the reference scenario in [README.md](README.md). Cultural acceptability depends on the actual audience, context and individual preferences; this rubric supplies questions and escalation rules, not universal facts about countries or religions. Do not infer a person's belief, identity, intentions or reaction from a word.

For every concern, retain the exact Chinese source, generated English, ID, system and available namespace. Identify the problematic phrase, a plausible consequence for the stated context, whether it originates in the source or translation, a proposed action and any missing evidence. Distinguish observed wording from an interpretation. A dictionary match alone cannot establish offense.

## Categories

| Category | Review question | Evidence required / guardrail |
| --- | --- | --- |
| `religion` | Does the text demean, exclude or misrepresent people because of belief? | Quote the claim or exclusion. A temple, wizard, spell or religious term alone is insufficient; ask for actual faith/community context when needed. |
| `cultural_stereotype` | Does it generalize traits to a real cultural, ethnic or national group? | Identify the real group and generalization. A game-group term such as tribe is not automatically a stereotype. Confirm glossary and visuals. |
| `identity_wording` | Does it invent or disparage gender, disability, family role or other identity? | Compare source and draft; do not treat all identity references as negative. Fictional species and real people require different context. |
| `age_context` | Does it add a threat, obscure age guidance, or change a relevant educational safety qualifier? | Quote the change and identify reader/setting. Combat metaphors and fantasy are not inherently disallowed. Confirm school policy and publisher claims. |
| `accessibility_inclusion` | Does it reverse or obscure an access feature or learner requirement? | Compare the feature meaning; distinguish a mistranslation from intentional prejudice. Verify real functionality before publishing claims. |
| `educational_tone` | Does it add shaming, unsupported certainty or discouragement? | Preserve source uncertainty and distinguish a fragment from a complete learner judgment. |
| `translation_quality` | Is it a meaning, name or terminology error with no demonstrated cultural consequence? | Route to quality review. Do not inflate cultural-risk counts with every mistranslation. |
| `commercial_localization` / `technical` | Are amounts, currency, billing periods, placeholders or tags changed? | Route to commercial/technical review. Never invent regional prices or convert currency without approved requirements. |
| `none` | Is no explicit concern evident within this narrow screen? | Record `no_signal`; do not equate this with safe, correct, approved or fully reviewed. |

Multiple categories use `|`. Each row has one primary action. Translation/commercial/technical issues may still block release without being cultural findings.

## Severity and action are separate

| Severity | Operational meaning | Expected action |
| --- | --- | --- |
| `0` | No explicit signal identified in available text | Retain for human check; no automatic clearance |
| `1` | Low-impact tone/precision concern | Propose editorial revision |
| `2` | Material concern for the reference setting, such as a threat or reversed accessibility requirement | Resolve before publication; seek owner approval for changes in meaning |
| `3` | Explicit group-based denigration/exclusion or comparably serious text | Escalate and revise before publication; no real-data severity-3 finding is asserted here |
| `U` | Severity cannot be responsibly assigned from the available evidence | Ask the recorded context question; do not substitute zero |
| `NA` | An issue is routed outside the cultural-severity scale | Resolve through quality/commercial/technical review |

Actions: `no_signal`, `revise`, `clarify`, `quality_only`. Severity is an **AI-proposed editorial priority**, not a measured harm score. The real table uses `0` only with `no_signal`, `U` only with `clarify`, `NA` only with `quality_only`, and `1`–`3` with `revise`.

## Review procedure

1. Confirm the deployment audience, read source and draft together, and inspect actual context where available.
2. Record concerns using the evidence rules. Missing optional context does not require marking every neutral UI label as a risk. Use `clarify` where a specific unresolved question changes the judgment.
3. Propose the smallest justified edit. Rewriting a source joke, family requirement, price or factual claim requires content-owner confirmation; do not silently present it as a faithful translation.
4. Separate “the translation removed a safety qualifier” from “the product is safe.” Neither the source nor this review establishes current safety, pricing, legal compliance or product functionality.
5. A named human reviewer records their own decision and actual timestamp. If two reviewers participate, preserve independent judgments before adjudication. No agreement statistic can be reported until those judgments exist.
6. Resolve technical constraints and retain the existing export gate. Cultural review never overrides a broken placeholder or tag.

## Guidance consulted and its limits

- [APA: general principles for reducing bias](https://apastyle.apa.org/style-grammar-guidelines/bias-free-language/general-principles) supports contextual precision and avoiding unnecessary identity assumptions. It is writing guidance, not a game certification standard.
- [APA: choosing words for talking about disability](https://www.apa.org/pi/disability/resources/choosing-words) explains that individual terminology preferences vary. This supports asking whether dwarf refers to a fantasy character or a person; it does not make that word categorically forbidden.
- [UNESCO: Manual for Developing Intercultural Competencies — Story Circles](https://unesdoc.unesco.org/ark:/48223/pf0000370336) motivates attention to the particular setting and participant backgrounds. It does not supply risk labels for these strings.

Consulted 2026-11-23. Categories, severity levels and individual annotations are project-specific proposals, not externally validated labels or a claim of compliance with these organizations.
