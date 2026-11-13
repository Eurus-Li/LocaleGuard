"""Train a small Marian LoRA adapter; select checkpoints on validation loss only."""
import argparse
import hashlib
import json
import math
import platform
import random
import time
import torch
from peft import LoraConfig, TaskType, get_peft_model
from transformers import MarianMTModel, MarianTokenizer, DataCollatorForSeq2Seq
from common import ROOT, MODEL_ID, MODEL_REVISION, model_input, read_jsonl

def main():
    p=argparse.ArgumentParser();p.add_argument('--base-model',default=MODEL_ID);p.add_argument('--epochs',type=int,default=3)
    p.add_argument('--batch-size',type=int,default=8);p.add_argument('--device',default='cpu');args=p.parse_args()
    torch.set_num_threads(4);torch.manual_seed(42);random.seed(42)
    tok=MarianTokenizer.from_pretrained(args.base_model,revision=MODEL_REVISION)
    base=MarianMTModel.from_pretrained(args.base_model,revision=MODEL_REVISION)
    base.config.use_cache=False
    model=get_peft_model(base,LoraConfig(task_type=TaskType.SEQ_2_SEQ_LM,r=8,lora_alpha=16,lora_dropout=.05,target_modules=['q_proj','v_proj'],bias='none')).to(args.device)
    model.print_trainable_parameters()
    def encode(split):
        rows=read_jsonl(ROOT/f'data/splits/{split}.jsonl');out=[]
        for r in rows:
            x=tok(model_input(r));x['labels']=tok(text_target=r['en'])['input_ids'];out.append(x)
        return out
    train=encode('train');valid=encode('validation');collate=DataCollatorForSeq2Seq(tok,model=model,padding=True)
    optimizer=torch.optim.AdamW((p for p in model.parameters() if p.requires_grad),lr=3e-4,weight_decay=.01)
    total=args.epochs*math.ceil(len(train)/args.batch_size);step=0;best=float('inf');history=[];start=time.time()
    def batch(items):return {k:v.to(args.device) for k,v in collate(items).items()}
    def validation_loss():
        model.eval();loss=0.;tokens=0
        with torch.no_grad():
            for i in range(0,len(valid),args.batch_size):
                b=batch(valid[i:i+args.batch_size]);n=int((b['labels']!=-100).sum());loss+=model(**b).loss.item()*n;tokens+=n
        return loss/tokens
    initial=validation_loss();print(json.dumps({'initial_validation_loss':initial}),flush=True)
    for epoch in range(args.epochs):
        random.shuffle(train);model.train();loss_sum=0.;nt=0
        for i in range(0,len(train),args.batch_size):
            b=batch(train[i:i+args.batch_size]);optimizer.zero_grad(set_to_none=True)
            warmup=max(1,int(total*.05));scale=min(1.,(step+1)/warmup)*max(.1,1-step/total)
            for g in optimizer.param_groups:g['lr']=3e-4*scale
            loss=model(**b).loss;loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.);optimizer.step()
            n=int((b['labels']!=-100).sum());loss_sum+=loss.item()*n;nt+=n;step+=1
            if step%25==0:print(json.dumps({'step':step,'total_steps':total,'epoch':epoch+1,'loss':round(loss.item(),4),'elapsed_seconds':round(time.time()-start,1)}),flush=True)
        val=validation_loss();entry={'epoch':epoch+1,'training_loss':loss_sum/nt,'validation_loss':val,'elapsed_seconds':time.time()-start};history.append(entry);print(json.dumps(entry),flush=True)
        if val<best:
            best=val;best_epoch=epoch+1
            model.save_pretrained(ROOT/'models/localeguard-marian-lora',safe_serialization=True)
    dest=ROOT/'models/localeguard-marian-lora'
    config=json.loads((dest/'adapter_config.json').read_text());config['base_model_name_or_path']=MODEL_ID;config['revision']=MODEL_REVISION
    (dest/'adapter_config.json').write_text(json.dumps(config,indent=2)+'\n')
    result={'seed':42,'base_model':MODEL_ID,'base_revision':MODEL_REVISION,'device':args.device,'platform':platform.platform(),'torch':torch.__version__,'epochs':args.epochs,'batch_size':args.batch_size,'optimizer':'AdamW','learning_rate':3e-4,'weight_decay':.01,'schedule':'5% warmup multiplied by linear decay with 0.1 floor','lora':{'r':8,'alpha':16,'dropout':.05,'target_modules':['q_proj','v_proj']},'trainable_parameters':sum(p.numel() for p in model.parameters() if p.requires_grad),'total_parameters_including_adapter':sum(p.numel() for p in model.parameters()),'initial_validation_loss':initial,'best_validation_loss':best,'selected_epoch':best_epoch,'history':history,'training_seconds':time.time()-start,'optimizer_steps':step,'adapter_sha256':hashlib.sha256((dest/'adapter_model.safetensors').read_bytes()).hexdigest(),'split_manifest_sha256':hashlib.sha256((ROOT/'data/splits/manifest.json').read_bytes()).hexdigest()}
    (ROOT/'training_run.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':main()
