import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap, RunnableLambda
import requests

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Load prompt
with open("prompts/extraction_prompt.txt", "r") as f:
    prompt_template = f.read()

prompt = PromptTemplate.from_template(prompt_template)


def mistral_api_call(prompt_text):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-medium",
        "messages": [{"role": "user", "content": prompt_text}],
        "temperature": 0.3
    }

    res = requests.post(url, headers=headers, json=data)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]


def get_chain():
    return (
        RunnableMap({
            "document": lambda x: x["document"],
            "instruction": lambda x: x["instruction"]
        })
        | prompt
        | RunnableLambda(lambda x: mistral_api_call(x.to_string()))
        | StrOutputParser()
    )



