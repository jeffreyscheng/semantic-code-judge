import requests
import os
# load in together api key from .env
from dotenv import load_dotenv
from core.constants import BASE_MODEL_NAME, VERIFICATION_SYSTEM_PROMPT, CODE_AUTHORING_SYSTEM_PROMPT
from core.data_ontology import SolutionCandidate

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
url = "https://api.together.xyz/v1/chat/completions"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {TOGETHER_API_KEY}"
}

def get_response(query: str, model_name: str = BASE_MODEL_NAME, system_prompt: str = VERIFICATION_SYSTEM_PROMPT):
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.text

def get_model_response_to_coding_prompt(
        prompt: str, model_name: str = BASE_MODEL_NAME
    ):
    return get_response(prompt, model_name=model_name, system_prompt=CODE_AUTHORING_SYSTEM_PROMPT)

def get_model_response_to_solution_candidate(candidate: SolutionCandidate, model_name: str = BASE_MODEL_NAME):
    return get_response(candidate.prompt + candidate.solution, model_name=model_name, system_prompt=VERIFICATION_SYSTEM_PROMPT)

def extract_model_answer_from_reasoning_trace(response: str):
    return response.split("Therefore, the candidate solution is ")[1].split(".")[0]

def format_reasoning_trace_for_model(prompt: str, solution: str, reasoning_trace: str):
    return f"<SystemPrompt> {VERIFICATION_SYSTEM_PROMPT} </SystemPrompt>" + \
        f"<User> {prompt + solution} </User>" + \
        f"<ReasoningTrace> {reasoning_trace} </ReasoningTrace>"