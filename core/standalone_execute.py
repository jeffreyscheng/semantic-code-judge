import tqdm
import re
import json
from core.standalone_unsafe_execute import unsafe_execute, UnresponsiveCodeExecutionError


def extract_code(model_generation: str) -> str:
    # Code is whatever is surrounded by triple backticks ```, or the whole answer.
    code_block_pattern = r"```(.*?)\n```"
    match = re.search(code_block_pattern, model_generation, re.DOTALL)
    if match:
        code = match.group(1)
        return code.strip().replace("```", "").removeprefix("python")
    else:
        return model_generation.replace("```", "").rstrip()


def execute_tests(
        function_header_and_docstring: str, model_generation: str, tests: list[str, ...]
) -> bool:
    """Returns whether the model generated code passes the given tests."""

    if len(tests) == 0:
        raise ValueError("No tests provided")

    implementation = function_header_and_docstring + "\n" + extract_code(model_generation)
    tests = "\n".join(tests)

    try:
        return unsafe_execute(implementation + "\n\n" + tests, timeout=10.0)
    except UnresponsiveCodeExecutionError as e:
        return False


if __name__ == "__main__":
    with open("train_synthetic_mbpp.jsonl", "r") as f:
        for i, line in tqdm.tqdm(enumerate(f)):
            line = json.loads(line)
            if not execute_tests(line["prompt"], line["solution"], line["tests"]):
                # Not all of the "solutions" are actually correct.
                print(i)