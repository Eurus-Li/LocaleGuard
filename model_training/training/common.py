"""LocaleGuard text preparation and deterministic quality checks."""
import collections
import html
import json
from pathlib import Path
import re

MODEL_ID = 'Helsinki-NLP/opus-mt-zh-en'
MODEL_REVISION = 'cf109095479db38d6df799875e34039d4938aaa6'
ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER = re.compile(r'__\w+__|\{\{[^{}]+\}\}|\$\{[^{}]+\}|\{[A-Za-z_][\w.]*\}|%(?:\d+\$)?[sdif]|%\d+|\$\d+')
TAG = re.compile(r'</?[A-Za-z][^>]*>')

def read_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding='utf-8').splitlines() if x.strip()]

def write_jsonl(path, rows):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in rows), encoding='utf-8')

def normalize(text):
    text = html.unescape(TAG.sub(' ', text)).lower()
    text = PLACEHOLDER.sub(' TOKEN ', text)
    return re.sub(r'[\W_]+', '', text)

def model_input(row, contextual=True):
    # Namespace is a weak context signal, not an invented scene or character.
    if not contextual: return row['zh_CN']
    return f"类别：{row['category']}。文本：{row['zh_CN']}"

def flags(source, translation, max_chars=None, glossary=None):
    problems = []
    if collections.Counter(PLACEHOLDER.findall(source)) != collections.Counter(PLACEHOLDER.findall(translation)):
        problems.append({'type':'placeholder', 'reason':'Placeholder multiset differs from the source.'})
    if TAG.findall(source) != TAG.findall(translation):
        problems.append({'type':'markup', 'reason':'HTML tag sequence or attributes differ from the source.'})
    if max_chars is not None and len(translation) > max_chars:
        problems.append({'type':'length', 'reason':f'Translation exceeds the supplied {max_chars}-character limit.'})
    if re.search(r'[\u3400-\u9fff]', translation):
        problems.append({'type':'untranslated', 'reason':'Chinese characters remain in the English draft.'})
    if not translation.strip(): problems.append({'type':'empty','reason':'The translation is empty.'})
    for term, target in (glossary or {}).items():
        if term in source and not re.search(r'(?<!\w)'+re.escape(target)+r'(?!\w)', translation, re.I):
            problems.append({'type':'terminology','reason':f'Review glossary term {term!r}; expected {target!r}.'})
    return problems

def choose_candidate(source, first, retry, **kwargs):
    # Minimize technical failures only; this is not a semantic-quality oracle.
    return retry if len(flags(source,retry,**kwargs)) < len(flags(source,first,**kwargs)) else first
