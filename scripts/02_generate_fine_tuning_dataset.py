from core.data_ontology import raw_starting_data
import hashlib
import json
import pandas as pd
import os
import random
import string
from core.data_ontology import SolutionCandidate
from core.model import extract_model_answer_from_reasoning_trace, format_reasoning_trace_for_model

def main():
    data = raw_starting_data
    prompt_records = []
    solutions_records = []
    reasoning_trace_records = []

    for candidate in data:
        prompt_hash = hashlib.md5(candidate.prompt.encode()).hexdigest().strip()
        solutions_hash = hashlib.md5(candidate.solution.encode()).hexdigest().strip()

        prompt_records.append({
            'prompt_hash': prompt_hash,
            'prompt': candidate.prompt,
            'tests': candidate.tests
        })
        solutions_records.append({
            'solution_hash': solutions_hash,
            'prompt_hash': prompt_hash,
            'solution': candidate.solution,
        })
    prompt_df = pd.DataFrame(prompt_records)
    solutions_df = pd.DataFrame(solutions_records)

    # ... rest of your processing code ...
    dirs = ['data/generated-reasoning-traces', 'data/handwritten-reasoning-traces']
    for dir in dirs:
        for file in os.listdir(dir):
            solution_hash = file.split('.')[0]
            reasoning_trace = open(os.path.join(dir, file), 'r').read()
            reasoning_trace_records.append({
                'solution_hash': solution_hash, 'reasoning_trace': reasoning_trace})
    
    # ... rest of your DataFrame operations ...
    reasoning_trace_df = pd.DataFrame(reasoning_trace_records)
    reasoning_trace_df['approved_by_model'] = reasoning_trace_df['reasoning_trace'].apply(extract_model_answer_from_reasoning_trace)

    joined_df = solutions_df.merge(reasoning_trace_df, on='solution_hash', how="inner")
    joined_df = joined_df.merge(prompt_df, on='prompt_hash', how="inner")

    joined_df['is_solution_correct'] = joined_df.apply(
        lambda row: SolutionCandidate(
            prompt=row['prompt'],
            solution=row['solution'],
            tests=row['tests']
        ).is_correct(),
        axis=1
    )

    joined_df['text'] = joined_df.apply(
        lambda row: format_reasoning_trace_for_model(row['prompt'], row['solution'], row['reasoning_trace']),
        axis=1
    )
    joined_df = joined_df[['text']]
    
    # Save files
    # count the number of files in the data/finetuning-files directory
    count = len(os.listdir('data/fine-tuning-files'))
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    joined_df.to_json(f'data/fine-tuning-files/fine-tuning-dataset-{count}-' + random_string + '.jsonl', orient='records', lines=True)

if __name__ == '__main__':
    main()