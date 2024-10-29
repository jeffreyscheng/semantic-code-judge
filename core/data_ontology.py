from dataclasses import dataclass
from typing import Optional
import json

@dataclass
class SolutionCandidate:
    prompt: str
    solution: str
    tests: str
    test_setup_lines: str
    reasoning_trace: Optional[str] = None
    
    def pretty_print(self):
        print(self.prompt)
        print(self.solution)

def read_data(file_path: str):
    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            yield SolutionCandidate(**data)

list(read_data('data/train_synthetic_mbpp.jsonl'))[1].pretty_print()
