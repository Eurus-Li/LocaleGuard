"""Translate JSONL inputs into review-required records; export only approved rows."""
import argparse
import json
import torch
from jsonschema import validate
from peft import PeftModel
from transformers import MarianMTModel, MarianTokenizer
from common import ROOT, MODEL_ID, MODEL_REVISION, model_input, flags, choose_candidate, read_jsonl, write_jsonl

SCHEMA={'type':'object','required':['id','source','translation','flags','status','attempts','cultural_review_required'],
 'properties':{'id':{'type':'string'},'source':{'type':'string'},'translation':{'type':'string'},'flags':{'type':'array','items':{'type':'object','required':['type','reason'],'properties':{'type':{'type':'string'},'reason':{'type':'string'}},'additionalProperties':False}},'status':{'const':'needs_review'},'attempts':{'type':'integer','minimum':1,'maximum':2},'cultural_review_required':{'const':True},'max_chars':{'type':'integer','minimum':1}},'additionalProperties':False}

def export_approved(rows,output,glossary=None):
    accepted=[]
    for row in rows:
        if row.get('status')!='approved':continue
        if not row.get('reviewer') or not row.get('reviewed_at'):raise ValueError('Approved rows need reviewer and reviewed_at.')
        remaining=flags(row['source'],row['translation'],row.get('max_chars'),glossary)
        if remaining:raise ValueError(f"{row['id']}: resolve technical flags before export: {remaining}")
        accepted.append({'id':row['id'],'translation':row['translation']})
    write_jsonl(output,accepted)

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.add_argument('--base-model',default=MODEL_ID);p.add_argument('--glossary');p.add_argument('--export-approved',action='store_true');a=p.parse_args()
    rows=read_jsonl(a.input);glossary=json.loads(open(a.glossary,encoding='utf-8').read()) if a.glossary else {}
    if a.export_approved:export_approved(rows,a.output,glossary);return
    torch.set_num_threads(4)
    tok=MarianTokenizer.from_pretrained(a.base_model,revision=MODEL_REVISION)
    model=PeftModel.from_pretrained(MarianMTModel.from_pretrained(a.base_model,revision=MODEL_REVISION),ROOT/'models/localeguard-marian-lora');model.eval()
    def translate(row,beams):
        x=tok(model_input(row),return_tensors='pt')
        if x['input_ids'].shape[1]>128:raise ValueError(f"{row['id']}: input exceeds the trained 128-token scope; split/review manually.")
        with torch.inference_mode():y=model.generate(**x,max_new_tokens=128,num_beams=beams,do_sample=False)
        return tok.decode(y[0],skip_special_tokens=True)
    out=[]
    for row in rows:
        h=translate(row,1);attempts=1;opts={'max_chars':row.get('max_chars'),'glossary':glossary}
        if flags(row['zh_CN'],h,**opts):
            h=choose_candidate(row['zh_CN'],h,translate(row,4),**opts);attempts=2
        result={'id':row['id'],'source':row['zh_CN'],'translation':h,'flags':flags(row['zh_CN'],h,**opts),'status':'needs_review','attempts':attempts,'cultural_review_required':True}
        # Retain the caller's constraint for revalidation during export.
        if row.get('max_chars') is not None:result['max_chars']=row['max_chars']
        validate(result,SCHEMA)
        out.append(result)
    write_jsonl(a.output,out)

if __name__=='__main__':main()
