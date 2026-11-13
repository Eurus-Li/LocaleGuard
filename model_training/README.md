# Model Training

Owner: **Eurus**. The first training run is complete. This folder contains the data, training code, adapter weights, and inference workflow.

| Location | Contents |
| --- | --- |
| [data/codecombat](data/codecombat/README.md) | Original and cleaned bilingual data, exclusions, provenance, license |
| [data/splits](data/splits/manifest.json) | Fixed training, validation, and test splits |
| [training](training/) | Preparation, training, prediction, common checks, dependencies |
| [models](models/localeguard-marian-lora/README.md) | Trained LoRA adapter and model card |
| [training_run.json](training_run.json) | Training settings and validation results |
| [examples](examples/) | Sample inputs and observed outputs |
| [docs/methodology.md](docs/methodology.md) | Methodology and limitations |
| [tests](tests/) | Pipeline checks |

Run commands from the repository root after installing `model_training/training/requirements.txt`:

```sh
python model_training/training/predict.py --input model_training/examples/input.jsonl --output outputs/drafts.jsonl
python -m unittest discover -s model_training/tests -v
```

To reproduce training (overwrites generated training artifacts):

```sh
python model_training/scripts/clean_codecombat.py
python model_training/training/prepare.py
python model_training/training/train.py --epochs 3 --device cpu
```

The adapter requires the pinned base model, which downloads separately. See the [main README](../README.md) for installation and approval/export instructions. Automatic comparison and human rating materials live in [evaluation](../evaluation/README.md); cultural/religious review lives in [cultural_risk_check](../cultural_risk_check/README.md).

## TODO

- [ ] Support teammates in running predictions and understanding the fixed data splits.
- [ ] Document model changes prompted by review; reserve fresh evaluation data if test feedback informs tuning.
- [ ] Keep model weights, provenance, and training records synchronized.
