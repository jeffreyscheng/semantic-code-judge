import requests
import os
# load in together api key from .env
from dotenv import load_dotenv
from constants import BASE_MODEL_NAME, SYSTEM_PROMPT
from data_ontology import SolutionCandidate

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
url = "https://api.together.xyz/v1/chat/completions"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {TOGETHER_API_KEY}"
}

def get_response(query: str, model_name: str = BASE_MODEL_NAME):
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.text

def get_model_response_to_solution_candidate(candidate: SolutionCandidate, model_name: str = BASE_MODEL_NAME):
    return get_response(candidate.prompt + candidate.solution, model_name=model_name)

def extract_model_answer_from_response(response: str):
    return response.split("Therefore, the candidate solution is ")[1].split(".")[0]