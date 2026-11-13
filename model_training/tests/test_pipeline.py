import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'training'))
from common import ROOT, flags, normalize, read_jsonl, choose_candidate
from predict import export_approved, SCHEMA
from jsonschema import validate, ValidationError

class PipelineTests(unittest.TestCase):
    def test_placeholder_multiplicity_and_tag_attributes(self):
        source='<a href="/play">你好 __name__，__name__！</a>'
        good='<a href="/play">Hello __name__, __name__!</a>'
        self.assertEqual(flags(source,good),[])
        self.assertIn('placeholder',[x['type'] for x in flags(source,good.replace(', __name__',''))])
        self.assertIn('markup',[x['type'] for x in flags(source,good.replace('/play','/other'))])

    def test_optional_constraints_and_retry(self):
        self.assertEqual(flags('等级','Level',max_chars=5,glossary={'等级':'level'}),[])
        self.assertIn('length',[x['type'] for x in flags('等级','Level',max_chars=4)])
        self.assertEqual(choose_candidate('你好 __name__','Hello','Hello __name__'),'Hello __name__')

    def test_human_gate_and_revalidation(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'out.jsonl'
            row={'id':'example','source':'你好 __name__','translation':'Hello __name__','status':'needs_review'}
            export_approved([row],out);self.assertEqual(out.read_text(),'')
            row.update(status='approved')
            with self.assertRaises(ValueError):export_approved([row],out)
            row.update(reviewer='test-reviewer',reviewed_at='test')
            export_approved([row],out);self.assertEqual(len(read_jsonl(out)),1)
            row['translation']='Hello'
            with self.assertRaises(ValueError):export_approved([row],out)

    def test_no_exact_cross_split_leakage(self):
        splits=[read_jsonl(ROOT/f'data/splits/{name}.jsonl') for name in ['train','validation','test']]
        for field in ['en','zh_CN','group_id']:
            sets=[set(normalize(r[field]) if field!='group_id' else r[field] for r in rows) for rows in splits]
            for i in range(3):
                for j in range(i):self.assertTrue(sets[i].isdisjoint(sets[j]),field)

    def test_json_schema_cannot_autoapprove(self):
        row={'id':'a','source':'你好','translation':'Hello','flags':[],'status':'needs_review','attempts':1,'cultural_review_required':True}
        validate(row,SCHEMA)
        row['status']='approved'
        with self.assertRaises(ValidationError):validate(row,SCHEMA)

if __name__=='__main__':unittest.main()
