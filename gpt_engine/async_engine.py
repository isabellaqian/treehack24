import os
import aiohttp
import asyncio
from dotenv import load_dotenv
import openai
from typing import List
import time
import json

# Load OpenAI API key from .env file
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

"""Make an asynchronous request to the OpenAI API with the given prompt."""


async def fetch_response(session, prompt, api_key, use_json=False):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    data = {
        "model": "gpt-3.5-turbo-0125",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 1,  # Adjust the parameters as needed
        "max_tokens": 4000,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }


    async with session.post(url, json=data, headers=headers, ssl=False) as response:
        response_data = await response.json()
        return response_data["choices"][0]["message"][
            "content"
        ]  # Extracting the text content


"""Process a list of prompts with asynchronous requests and return the list of responses."""


async def process_prompts(api_key, prompts, use_json=False):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for prompt in prompts:
            tasks.append(fetch_response(session, prompt, api_key, use_json=use_json))

        return await asyncio.gather(*tasks)


"""Function to be called by users with a list of strings. Returns a list of response strings."""


def get_openai_responses(prompts: List[str], use_json=False) -> List[str]:
    # Ensure the API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenAI API Key is required. Haven't found in the env variable"
        )

    # Process the prompts and get responses
    responses = asyncio.run(process_prompts(api_key, prompts, use_json))

    return responses


# Test
if __name__ == "__main__":
    # Example prompts
    my_prompts = [
        "What is the capital of France?",
        "Explain the theory of relativity in simple terms."
        # Add as many prompts as you want here
    ]

    responses = get_openai_responses(my_prompts)

    # Displaying responses (or you can process the responses as needed)
    for prompt, response in zip(my_prompts, responses):
        print(f"Prompt: {prompt}")
        print(f"Response: {response}\n")
