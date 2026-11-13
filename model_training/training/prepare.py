"""Freeze length-bounded, grouped splits before any training or evaluation."""
import argparse
import collections
import difflib
import hashlib
import json
import random
import re
from transformers import MarianTokenizer
from common import ROOT, MODEL_ID, MODEL_REVISION, normalize, model_input, read_jsonl, write_jsonl

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--base-model',default=MODEL_ID)
    args=parser.parse_args()
    tok=MarianTokenizer.from_pretrained(args.base_model,revision=MODEL_REVISION)
    path=ROOT/'data/codecombat/cleaned_data.jsonl';rows=read_jsonl(path)
    valid=[];excluded=[]
    for row in rows:
        ns=len(tok(model_input(row))['input_ids']);nt=len(tok(text_target=row['en'])['input_ids'])
        if ns>128 or nt>128:
            excluded.append({'id':row['id'],'reason':'over_128_tokens','source_tokens':ns,'target_tokens':nt})
        elif not normalize(row['zh_CN']) or not normalize(row['en']):
            excluded.append({'id':row['id'],'reason':'empty_normalized_text'})
        else:valid.append(row)
    parent=list(range(len(valid)))
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    def union(i,j):parent[find(i)]=find(j)
    # Exact source OR target matches and high-similarity strings stay together.
    # Pairwise comparisons are bounded by length and token overlap.
    for lang in ['zh_CN','en']:
        seen={};texts=[normalize(r[lang]) for r in valid]
        for i,t in enumerate(texts):
            if t in seen:union(i,seen[t])
            seen[t]=i
        index=collections.defaultdict(set)
        for i,t in enumerate(texts):
            if len(t)<12:continue
            grams={t[j:j+4] for j in range(len(t)-3)};candidates=collections.Counter()
            for g in grams:
                for j in index[g]:candidates[j]+=1
            for j,overlap in candidates.items():
                u=texts[j]
                if min(len(t),len(u))/max(len(t),len(u))<.9:continue
                if overlap/max(1,len(grams))<.75:continue
                if difflib.SequenceMatcher(None,t,u,autojunk=False).ratio()>=.92:union(i,j)
            for g in grams:index[g].add(i)
    groups=collections.defaultdict(list)
    for i,r in enumerate(valid):groups[find(i)].append(r)
    items=list(groups.values());random.Random(42).shuffle(items)
    splits={'train':[],'validation':[],'test':[]}
    for group in items:
        split='test' if len(splits['test'])<200 else 'validation' if len(splits['validation'])<200 else 'train'
        group_id=hashlib.sha256('\n'.join(sorted(r['id'] for r in group)).encode()).hexdigest()[:16]
        splits[split].extend({**r,'group_id':group_id} for r in group)
    for split,records in splits.items():write_jsonl(ROOT/f'data/splits/{split}.jsonl',records)
    write_jsonl(ROOT/'data/splits/excluded.jsonl',excluded)
    assert set(r['group_id'] for r in splits['train']).isdisjoint(r['group_id'] for r in splits['test'])
    for lang in ['en','zh_CN']:
        sets=[set(normalize(r[lang]) for r in splits[s]) for s in splits]
        assert all(sets[i].isdisjoint(sets[j]) for i in range(3) for j in range(i))
    manifest={'seed':42,'model':MODEL_ID,'revision':MODEL_REVISION,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'input_rows':len(rows),'excluded':len(excluded),'split_sizes':{k:len(v) for k,v in splits.items()},'groups':len(groups),'max_source_tokens':128,'max_target_tokens':128,'grouping':'Exact normalized source OR target; plus length-ratio >= .9, character-4gram candidate overlap >= .75, SequenceMatcher >= .92. Group assignment is deterministic, not stratified. This heuristic does not guarantee removal of all semantic near-duplicates.'}
    (ROOT/'data/splits/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))

if __name__=='__main__':main()
