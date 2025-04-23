# Download MMLU dataset from HuggingFace 
from datasets import load_dataset

# Load specific MMLU tasks
tasks = ['anatomy', 'astronomy', 'college_biology', 'college_chemistry', 'prehistory']

datasets = {}
for task in tasks:
  dataset = load_dataset("cais/mmlu", task)
  datasets[task] = dataset
  
  # Save to disk
  for split in ['train', 'validation', 'test']:
    if split in dataset:
      dataset[split].to_json(f"mmlu_datasets/mmlu_{task}_{split}.json")