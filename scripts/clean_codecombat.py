"""Rebuild cleaned_data.jsonl and exclusion records from original_pairs.jsonl.

Usage: python scripts/clean_codecombat.py [data-directory]
Uses only the Python standard library. Original text is preserved in output.
"""
import collections
import html
import json
from pathlib import Path
import re
import sys

def normalized(text):
    # Used only for comparison, never to overwrite exported translations.
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]*>', ' ', text))).strip()

def exclusion_reason(en, zh):
    if not en.strip() or not zh.strip(): return 'empty'
    if '[AI_TRANSLATION]' in en or '[AI_TRANSLATION]' in zh: return 'AI_TRANSLATION'
    if any(re.search(r'\(used in [^)]+\)', s, re.I) for s in (en, zh)): return 'locale_placeholder'
    if normalized(en) == normalized(zh): return 'identical'
    if not re.search(r'[\u3400-\u9fff]', zh): return 'no_chinese_characters'
    if not re.search(r'[A-Za-z]', normalized(en)): return 'no_english_letters'
    return None

def write_jsonl(path, rows):
    path.write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows), encoding='utf-8')

def clean(rows):
    ids = [row['id'] for row in rows]
    if len(ids) != len(set(ids)): raise ValueError('Duplicate source IDs')
    kept, excluded, seen = [], [], {}
    for row in rows:
        en, zh = row['en'], row['zh_CN']
        if not isinstance(en, str) or not isinstance(zh, str): raise ValueError(row['id'])
        reason = exclusion_reason(en, zh)
        pair = (normalized(en), normalized(zh))
        if reason:
            excluded.append({'id': row['id'], 'reason': reason})
        elif pair in seen:
            excluded.append({'id': row['id'], 'reason': 'duplicate_pair', 'duplicate_of': seen[pair]})
        else:
            seen[pair] = row['id']
            kept.append(row)
    return kept, excluded

def main():
    directory = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'data' / 'codecombat'
    rows = [json.loads(line) for line in (directory / 'original_pairs.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    kept, excluded = clean(rows)
    write_jsonl(directory / 'cleaned_data.jsonl', kept)
    write_jsonl(directory / 'excluded_records.jsonl', excluded)
    summary = {'original_pairs': len(rows), 'cleaned_pairs': len(kept), 'excluded_pairs': len(excluded),
               'exclusion_counts': dict(sorted(collections.Counter(x['reason'] for x in excluded).items()))}
    (directory / 'cleaning_report.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))

if __name__ == '__main__': main()
