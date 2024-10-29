# semantic-code-judge

To generate a new fine-tuning dataset from existing model code implementations and model reasoning traces:
```
python scripts/generate_fine_tuning_dataset.py
```

To generate a new fine-tuning dataset from scratch:
```
python scripts/generate_code_implementations_from_llm.py && python scripts/generate_fine_tuning_dataset.py
```

To fine-tune a model:
```
python scripts/fine_tune_model.py
```

To evaluate the fine-tuned model:
```
python scripts/evaluate_model.py
```