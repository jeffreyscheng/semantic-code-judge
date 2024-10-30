from dataclasses import dataclass
from typing import Optional
from core.standalone_execute import execute_tests
import json
import time

@dataclass
class SolutionCandidate:
    prompt: str
    solution: str
    tests: str
    test_setup_lines: Optional[list[str]] = None
    reasoning_trace: Optional[str] = None
    
    def pretty_print(self):
        print(self.prompt)
        print(self.solution)

    def is_correct(self):
        tick = time.time()
        result = execute_tests(self.prompt, self.solution, self.tests)
        tock = time.time()
        print(f"Execution time: {tock - tick} seconds")
        return result

def read_data(file_path: str):
    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            yield SolutionCandidate(**data)

raw_starting_data = list(read_data('data/train_synthetic_mbpp.jsonl'))
# list(read_data('data/train_synthetic_mbpp.jsonl'))[1].pretty_print()

# data = list(read_data('data/train_synthetic_mbpp.jsonl'))
# for candidate in data:
#     if candidate.test_setup_lines:
#         candidate.pretty_print()
#         print(candidate.test_setup_lines)
#         raise ValueError('unimplemented')
