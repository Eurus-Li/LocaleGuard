# Validation record

Performed 2026-11-23 using Python 3 and the standard library.

## Passed consistency checks

```text
PASS: input hashes and Git blobs; 200 exact real rows; 32 exact comparison rows; 8 separate synthetic rows;
      categories, actions, severities, pending sign-offs, summary counts, and local Markdown links.
```

Command from the repository root:

```sh
python3 cultural_risk_check/validate_review.py
```

Both input Git blob SHAs were also fetched at the pinned baseline commit and matched the files used for this review. All 800 original prediction records match their fixed test source/reference. The review table contains each of the 200 LocaleGuard IDs once, in stored order. The comparison table contains eight IDs once per system. AI annotations and synthetic expectations remain separate from actual model evidence.

Three deliberate-corruption checks were run in temporary copies, leaving deliverables unchanged:

| Deliberate corruption | Observed validator response |
| --- | --- |
| Change a reviewed translation | Rejected: altered translation |
| Fill a human reviewer field while sign-off is pending | Rejected: invented human sign-off |
| Change summary coverage to 201 | Rejected: wrong real-data count |

## What these checks do not establish

Passing validates data consistency and the stated workflow boundaries. It does not prove that the AI labels are culturally correct, that an audience will react in a particular way, that external links remain available, that actual UI rendering is correct, or that product safety, functionality, event terms and prices are current. Human validation is pending. The original model was not rerun, and no source/test/model metric files were modified.
