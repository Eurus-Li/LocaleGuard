"""Compare fixed systems on the frozen held-out test set. No test tuning."""
import argparse
import collections
import csv
import json
import random
import time
import torch
from peft import PeftModel
from sacrebleu.metrics import BLEU, CHRF
from transformers import MarianMTModel, MarianTokenizer
from common import ROOT, MODEL_ID, MODEL_REVISION, model_input, flags, choose_candidate, read_jsonl, write_jsonl, PLACEHOLDER, TAG

def generate(model,tok,rows,contextual,beams=1,batch_size=8):
    outputs=[];start=time.time()
    model.eval()
    with torch.inference_mode():
        for i in range(0,len(rows),batch_size):
            batch=tok([model_input(r,contextual) for r in rows[i:i+batch_size]],return_tensors='pt',padding=True)
            out=model.generate(**batch,max_new_tokens=128,num_beams=beams,do_sample=False)
            outputs.extend(tok.batch_decode(out,skip_special_tokens=True))
    return outputs,time.time()-start

def main():
    p=argparse.ArgumentParser();p.add_argument('--base-model',default=MODEL_ID);args=p.parse_args()
    torch.set_num_threads(4);torch.manual_seed(42)
    rows=read_jsonl(ROOT/'data/splits/test.jsonl');tok=MarianTokenizer.from_pretrained(args.base_model,revision=MODEL_REVISION)
    base=MarianMTModel.from_pretrained(args.base_model,revision=MODEL_REVISION);base.config.use_cache=True
    systems={};times={};attempts={}
    for name,context in [('base_direct',False),('base_context',True)]:
        systems[name],times[name]=generate(base,tok,rows,context)
        print(json.dumps({'completed':name,'seconds':times[name]}),flush=True)
    model=PeftModel.from_pretrained(base,ROOT/'models/localeguard-marian-lora');model.eval()
    systems['finetuned_context'],times['finetuned_context']=generate(model,tok,rows,True)
    print(json.dumps({'completed':'finetuned_context','seconds':times['finetuned_context']}),flush=True)
    bad=[i for i,(r,h) in enumerate(zip(rows,systems['finetuned_context'])) if flags(r['zh_CN'],h)]
    retries,retry_seconds=generate(model,tok,[rows[i] for i in bad],True,beams=4)
    guarded=systems['finetuned_context'].copy()
    for i,retry in zip(bad,retries):guarded[i]=choose_candidate(rows[i]['zh_CN'],guarded[i],retry)
    systems['localeguard']=guarded;times['localeguard']=times['finetuned_context']+retry_seconds
    bleu=BLEU();chrf=CHRF(word_order=2);references=[[r['en'] for r in rows]];metrics={};predictions=[]
    for name,hyps in systems.items():
        checks=[flags(r['zh_CN'],h) for r,h in zip(rows,hyps)]
        placeholder_rows=sum(bool(PLACEHOLDER.search(r['zh_CN'])) for r in rows)
        markup_rows=sum(bool(TAG.search(r['zh_CN'])) for r in rows)
        metrics[name]={'bleu':bleu.corpus_score(hyps,references).score,'chrf_plus_plus':chrf.corpus_score(hyps,references).score,'exact_match_count':sum(h.strip()==r['en'].strip() for r,h in zip(rows,hyps)),'flagged_rows':sum(bool(f) for f in checks),'flag_counts':dict(collections.Counter(f['type'] for fs in checks for f in fs)),'source_rows_with_placeholders':placeholder_rows,'source_rows_with_markup':markup_rows,'inference_seconds':times[name],'seconds_per_string':times[name]/len(rows),'retry_count':len(bad) if name=='localeguard' else 0}
        for r,h,fs in zip(rows,hyps,checks):predictions.append({'id':r['id'],'category':r['category'],'source':r['zh_CN'],'reference':r['en'],'system':name,'translation':h,'flags':fs,'status':'needs_review'})
    result={'test_rows':len(rows),'systems':metrics,'bleu_signature':str(bleu.get_signature()),'chrf_signature':str(chrf.get_signature()),'generation':{'max_new_tokens':128,'initial_num_beams':1,'retry_num_beams':4,'max_retries':1},'length_limits':'No original character limits available; not fabricated or scored.','human_evaluation':'Not performed: quality ratings, review time, edits, cultural flags, and false alarms require human reviewers.','cost':'No paid API used. Local hardware/electricity costs not measured. Cost per accepted string is unavailable without approvals.','comparison_limit':'Base-context uses a prefix with a translation model not instruction-trained. Fine-tuning and prefix adaptation are confounded in base-context versus fine-tuned-context; no causal claim about context alone.'}
    (ROOT/'evaluation/metrics.json').write_text(json.dumps(result,indent=2)+'\n');write_jsonl(ROOT/'evaluation/test_predictions.jsonl',predictions)
    review=predictions.copy();random.Random(42).shuffle(review);key=[]
    fields=['review_id','string_id','source','reference','translation','meaning_1_to_5','fluency_1_to_5','terminology_1_to_5','cultural_issue','review_seconds','edited_translation','accept','notes']
    with (ROOT/'evaluation/blind_review.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for i,r in enumerate(review):
            rid=f'R{i+1:04d}';w.writerow({'review_id':rid,'string_id':r['id'],'source':r['source'],'reference':r['reference'],'translation':r['translation']});key.append({'review_id':rid,'system':r['system'],'id':r['id']})
    write_jsonl(ROOT/'evaluation/review_key.jsonl',key)
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':main()
