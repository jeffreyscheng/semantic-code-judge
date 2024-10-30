import hashlib

from core.data_ontology import raw_starting_data, SolutionCandidate
from core.model import get_model_response_to_coding_prompt
from core.constants import BASE_MODEL_NAME

MODEL = BASE_MODEL_NAME
for candidate in raw_starting_data:
    prompt_hash = hashlib.md5(candidate.prompt.encode()).hexdigest()
    model_code = get_model_response_to_coding_prompt(candidate.prompt)
    # save


