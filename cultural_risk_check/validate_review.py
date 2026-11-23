"""Validate this versioned review package; does not validate cultural judgments."""
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_csv(name):
    with (HERE / name).open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        require(len(reader.fieldnames) == len(set(reader.fieldnames)), f'{name}: duplicate columns')
        rows = list(reader)
    require(rows and all(None not in r and all(v is not None for v in r.values()) for r in rows),
            f'{name}: malformed or empty CSV')
    return rows


def main():
    manifest = json.loads((HERE/'provenance.json').read_text())
    for path, expected in manifest['inputs'].items():
        data = (ROOT/path).read_bytes()
        require(hashlib.sha256(data).hexdigest() == expected['sha256'], f'{path}: SHA-256 mismatch')
        blob = b'blob ' + str(len(data)).encode() + b'\0' + data
        require(hashlib.sha1(blob).hexdigest() == manifest['upstream_git_blob_shas'][path],
                f'{path}: upstream Git blob mismatch')
        require(f"/blob/{manifest['baseline_commit']}/" in expected['github_url'], f'{path}: unpinned source')

    predictions = [json.loads(s) for s in (ROOT/'evaluation/test_predictions.jsonl').read_text().splitlines()]
    tests = [json.loads(s) for s in (ROOT/'model_training/data/splits/test.jsonl').read_text().splitlines()]
    require(len(tests) == 200 and len({r['id'] for r in tests}) == 200, 'Expected 200 unique held-out IDs')
    by_test = {r['id']: r for r in tests}
    systems = {'base_direct','base_context','finetuned_context','localeguard'}
    require(Counter(r['system'] for r in predictions) == Counter({s:200 for s in systems}),
            'Unexpected system coverage')
    by_prediction = {(r['id'],r['system']):r for r in predictions}
    require(len(by_prediction) == 800, 'Duplicate prediction key')
    for r in predictions:
        require(r['source'] == by_test[r['id']]['zh_CN'], f"{r['id']}: prediction source mismatch")
        require(r['reference'] == by_test[r['id']]['en'], f"{r['id']}: prediction reference mismatch")

    rows = read_csv('review_table.csv')
    require(len(rows) == 200 and len({r['id'] for r in rows}) == 200, 'Review must cover 200 unique IDs')
    expected_order = [r['id'] for r in predictions if r['system'] == 'localeguard']
    require([r['id'] for r in rows] == expected_order, 'Review order/coverage differs from LocaleGuard inputs')
    action_severity = {'no_signal':{'0'},'clarify':{'U'},'quality_only':{'NA'},'revise':{'1','2','3'}}
    categories = {'none','religion','cultural_stereotype','identity_wording','age_context',
                  'accessibility_inclusion','educational_tone','translation_quality','commercial_localization','technical'}
    for r in rows:
        require(r['system'] == 'localeguard', f"{r['id']}: unexpected review system")
        p = by_prediction[(r['id'],r['system'])]
        for field in ('source','reference','translation'):
            require(r[field] == p[field], f"{r['id']}: altered {field}")
        require(r['namespace_context'] == p['category'], f"{r['id']}: invented namespace")
        require(json.loads(r['technical_flags']) == p['flags'], f"{r['id']}: changed technical flags")
        require(r['decision'] in action_severity and r['severity'] in action_severity[r['decision']],
                f"{r['id']}: invalid action/severity")
        require(set(r['risk_category'].split('|')) <= categories, f"{r['id']}: invalid category")
        for field in ('rationale','context_question','audience_assumption','annotation_method','annotator','review_date'):
            require(bool(r[field].strip()), f"{r['id']}: missing {field}")
        require(r['review_date'] == manifest['review_date'], f"{r['id']}: inconsistent date")
        require('AI' in r['annotator'] and 'unblinded' in r['annotation_method'], 'Missing AI/method disclosure')
        require(r['human_review_status'] == 'pending' and not any(r[k] for k in
                ('human_reviewer','human_reviewed_at','human_decision')), f"{r['id']}: invented human sign-off")
        if r['decision'] == 'revise':
            require(bool(r['suggested_revision'].strip()), f"{r['id']}: revision without proposal")
        require(not r['id'].startswith('SYN-'), 'Synthetic data mixed into real review')

    comparison = read_csv('case_comparisons.csv')
    require(len(comparison) == 32 and len({r['id'] for r in comparison}) == 8, 'Expected 8 x 4 comparisons')
    require(len({(r['id'],r['system']) for r in comparison}) == 32, 'Duplicate comparison key')
    for id in {r['id'] for r in comparison}:
        require({r['system'] for r in comparison if r['id'] == id} == systems, f'{id}: missing comparison system')
    for r in comparison:
        p = by_prediction[(r['id'],r['system'])]
        require(all(r[k] == p[k] for k in ('source','reference','translation')), f"{r['id']}: altered case evidence")
        require(json.loads(r['technical_flags']) == p['flags'], f"{r['id']}: altered case flags")

    challenge = read_csv('challenge_set.csv')
    require(len(challenge) == 8 and len({r['id'] for r in challenge}) == 8, 'Expected eight unique synthetic rows')
    for r in challenge:
        require(r['id'].startswith('SYN-') and r['id'] not in by_test, 'Synthetic ID collision')
        require(r['data_origin'] == 'synthetic_challenge_not_model_output', 'Missing synthetic disclosure')
        require(r['expected_action'] in action_severity and
                r['expected_severity'] in action_severity[r['expected_action']], 'Invalid challenge expectation')
        require(set(r['expected_category'].split('|')) <= categories, 'Invalid challenge category')
        require('pending human validation' in r['label_status'], 'Challenge label overstated')

    summary = json.loads((HERE/'summary.json').read_text())
    require(summary['real_unique_ids'] == len(rows), 'Wrong real-data count')
    require(summary['decision_counts'] == dict(Counter(r['decision'] for r in rows)), 'Wrong action counts')
    require(summary['severity_counts'] == dict(Counter(r['severity'] for r in rows)), 'Wrong severity counts')
    require(summary['human_approved_rows'] == 0, 'Overstated human approval')
    require(summary['case_comparison_rows'] == len(comparison) and summary['case_comparison_ids'] == 8,
            'Wrong comparison counts')
    require(summary['synthetic_challenge_rows'] == len(challenge) and
            summary['synthetic_model_inference_performed'] is False, 'Overstated synthetic results')
    require(summary['baseline_commit'] == manifest['baseline_commit'], 'Mismatched baseline')
    for path in HERE.glob('*.md'):
        text = path.read_text()
        require(text.count('```') % 2 == 0, f'{path.name}: unbalanced code fences')
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if target.startswith(('https://','http://','#','mailto:')):
                continue
            require((path.parent/unquote(target.split('#')[0])).is_file(), f'{path.name}: broken local link {target}')
    print('PASS: input hashes and Git blobs; 200 exact real rows; 32 exact comparison rows; 8 separate synthetic rows;')
    print('      categories, actions, severities, pending sign-offs, summary counts, and local Markdown links.')
    print('Human cultural correctness, external-site availability, UI rendering and product claims are not validated.')


if __name__ == '__main__':
    main()
