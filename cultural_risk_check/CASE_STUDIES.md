# Case studies and findings

AI-assisted, unblinded text review · 2026-11-23 · human validation pending.

## What was reviewed

All **200 LocaleGuard drafts** from the fixed test set were screened against their Chinese source and stored English reference. The eight comparison IDs were chosen purposively for interpretability, inclusion, tone, acceptable controls and technical limitations. The [32-row evidence file](case_comparisons.csv) preserves all four existing system outputs for those IDs. It is not a random sample, blind evaluation or cultural leaderboard. The [provenance manifest](provenance.json) pins input versions.

## Representative real cases

| ID / observed wording | Finding and proposed treatment | Boundary / missing context |
| --- | --- | --- |
| `galaxy.locked_by_teacher`: 已被教师锁定 → `already locked by teacher` | The LocaleGuard draft avoids the base-direct draft's `She's locked in by the teacher.` The base draft invents gender and can suggest a person being confined. Keep the LocaleGuard row as a `no_signal` control for this narrow issue. | Only this case is observed. It does not establish a measured reduction in gender bias or identify the locked UI element. |
| `clans.create_clan`: 创建新的部落 → `Create a new tribe` | `clarify`, severity `U`. Reference `Create New Clan` and namespace `clans` support using the feature name Clan consistently. The same question applies to `clans.private_clans`. | Tribe alone is not evidence of derogation. Confirm feature glossary and visuals; no real community or stereotype has been established. |
| `play_level.tip_munchkin`: 如果您不吃掉您的蔬菜, 一个小矮人将在您睡着之后来找您。 → `If you do not eat your vegetables, a dwarf will come to you after you fall asleep.` | `revise`, severity `2`. The bedtime threat originates in the source and persists in all four outputs. Propose an encouraging food/break reminder with owner approval. | Do not label dwarf categorically offensive. It may denote a fantasy being. Character art and educator judgment are missing; changing the joke is a content adaptation. |
| `junior_page.with_our_tablet_friendly_platform`: 无需阅读和打字的选项 → `non-readable and typed options` within the full draft | `revise`, severity `2`. The draft changes a no-reading/no-typing access feature into an unclear, partly reversed requirement. Restore that feature meaning. | This is adult-facing Junior copy about younger learners. Actual device support and accessibility claims still require product-owner verification. No intentional discrimination is inferred. |
| `legal.archmage_wiki_url`: 我们大法师的维基页 → `Wiki Pages of Our Great Master` | `quality_only`, severity `NA`. Proposed wording: `our Archmage wiki`, subject to checking the named contributor role. | There is no basis to infer an insult to a real faith. Base drafts also substitute WikiLeaks; that is a naming/meaning error, not evidence of religious risk. |
| `announcement.pugicorn_description`: 巴哥犬是一些最稀有的生物，可以施展法术！ → `Bargo Dogs are some of the rarest creatures to be able to perform magic!` | `no_signal`, severity `0` for the narrow cultural screen. Magic in fantasy is not automatically religious denigration. | The creature name is a separate quality issue; no school policy banning fantasy has been supplied. This is not publication approval. |
| `parents_landing_2.private_classes_price`: $219/月或$399/月 → `$219 or $399` | `quality_only`, severity `NA`. Both prices remain but `/month` is omitted. Proposed dataset-faithful edit: `$219/month or $399/month`. | LocaleGuard flags are empty. Do not interpret that as semantic or commercial correctness; current prices and currency are unverified. |
| `special_offer.low_price_title`: 每个学生仅仅只要 __starterLicensePrice__ 元 → `Each student only needs __StarterLiceSimple__` | `quality_only`, severity `NA`. The checker does flag the corrupted placeholder. Restore the exact token and verify the source currency; a provisional yuan wording is recorded. | A US reference scenario does not authorize dollar substitution, currency conversion or regional pricing changes. |

The proposed wording and per-row context questions are in [review_table.csv](review_table.csv). Full strings, including the long accessibility example, are retained there; quoted fragments above are explanatory excerpts.

## Other escalations in the 200-row screen

- `play.campaign_multiplayer_description` and `ladder.tournament_blurb` need classroom-tone/context clarification. A combat metaphor is not automatically harmful; the latter's historical prize claim also needs current event terms before republication. No gambling claim is made.
- `new_premium.carousel_items_5_text` omits a source safety/environment qualifier. `hackstack_page.faq_1_answer` changes the subject of an age-suitability claim and mistranslates multimodal. These require meaning corrections and verification of the source claims, not a safety certification.
- `teacher.student_warn` loses the tentative 可能. Preserve uncertainty in teacher-facing language.
- Additional noted quality issues include `teachers.programming_language_edit_desc_new`, `subscribe.yearly_inspire` and `amazon_hoc.title`. The savings example has a source/reference mismatch; copying the English reference's discount percentage would not faithfully translate the Chinese amount.

## Counts and interpretation

The real table contains **5 `revise`, 4 `clarify`, 6 `quality_only`, 185 `no_signal`** rows. Severity totals are **185 at `0`, 1 at `1`, 4 at `2`, 4 at `U`, 6 at `NA`**; no real-data severity `3` is assigned. These are descriptive AI judgments. They cannot establish the true rate of cultural risk, the total translation-error count or cultural competence of any system. All 200 rows still have pending human review.

No explicit real-faith denigration is asserted in the reviewed data. The absence of such a finding does not demonstrate comprehensive religious safety. A separate [eight-row synthetic challenge set](challenge_set.csv) includes neutral religious references, a derogatory invented candidate, fantasy controls, terminology ambiguity, accessibility reversal, gender invention and a commercial/technical negative control. These were **not run through the translation model**; their expected actions are proposed reviewer exercises, not measured predictions, test-set additions or evidence of detector accuracy.

## Limits and next decisions

This is one AI reviewer, one unblinded reading, one fixed dataset and one assumed reference setting. Scene, speaker, character art, surrounding strings, rendering, actual user reactions and school policies are missing. There are no independent human judgments, inter-rater agreement, review-time measurements, accepted edits or live-game tests. An empty technical flag list is not a meaning check. No source, model weight, test split, prediction file, automatic metric or approval record was changed.

A bilingual human should review the five revision proposals, resolve the four context questions, address the noted quality/technical issues, and spot-check the remaining rows before publication. Broader markets require locally informed review. Any future use of these findings for tuning should be evaluated on fresh held-out data. The strongest supported claim today is: **a traceable cultural-review package and AI-assisted preliminary screen are complete; human validation is pending**.
