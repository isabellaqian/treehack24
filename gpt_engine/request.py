import os, time
import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Union, Set
from .async_engine import get_openai_responses


# Custom exception for clarity in error handling.
class FileNotFoundError(Exception):
    pass


# Util function to read and replace content from a file.
def read_and_fill_template(
    file_path: str, replacements: Dict[str, str]
) -> Union[str, None]:
    """Reads a file and replaces placeholders with actual content."""
    try:
        with open(file_path, "r") as file:
            content = file.read()
    except IOError:
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    for placeholder, value in replacements.items():
        content = content.replace(f"{{{placeholder}}}", value)

    return content


# Util function to parse JSON string.
def parse_json(json_string: str) -> Union[Dict, None]:
    """Converts a JSON string into a dictionary."""
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


# Validate the necessary fields in the parsed JSON.
def validate_json_fields(parsed_json: Dict, required_fields: Set[str]) -> bool:
    """Checks if the provided fields match the required ones in the JSON dictionary."""
    actual_fields = set(parsed_json.keys())

    if actual_fields != required_fields:
        missing = required_fields - actual_fields
        extra = actual_fields - required_fields

        if missing:
            print(f"Missing fields: {', '.join(missing)}")
        if extra:
            print(f"Extra fields: {', '.join(extra)}")
        return False

    return True


# Main function to process the GPT-4 response.
def process_gpt_response(
    prompt_name: str,
    user_input: dataclass,
    required_fields: Set[str],
    use_json: bool = True,
) -> Dict:
    """Sends prompt to GPT-4, receives response, and processes the information."""
    input_dict = user_input
    current_dir = os.path.abspath(os.path.dirname(__file__))
    prompt_path = os.path.join(current_dir, f"prompts/{prompt_name}.txt")

    # Prepare the prompt
    prompt = read_and_fill_template(prompt_path, input_dict)
    if prompt is None:
        raise FileNotFoundError("Prompt file not found or failed to read.")

    # Communicate with GPT-4 and get the response
    responses = get_openai_responses([prompt], use_json=use_json)

    return responses


def parallel_request(prompt_name: str, user_inputs: List[dataclass]) -> List[dict]:
    """Sends prompt to GPT-4, receives response, and processes the information."""
    current_dir = os.path.abspath(os.path.dirname(__file__))
    prompt_path = os.path.join(current_dir, f"prompts/{prompt_name}.txt")

    # Prepare the prompt
    prompts = list()
    for user_input in user_inputs:
        input_dict = asdict(user_input)
        prompt = read_and_fill_template(prompt_path, input_dict)
        prompts.append(prompt)
    # Communicate with GPT-4 and get the response
    responses = get_openai_responses(prompts)
    response_jsons = [parse_json(response) for response in responses]

    return response_jsons


def process_gpt_response_list(
    prompt_name: str,
    user_input: dataclass,
    required_fields: Set[str],
    use_json: bool = True,
):
    input_dict = asdict(user_input)
    current_dir = os.path.abspath(os.path.dirname(__file__))
    prompt_path = os.path.join(current_dir, f"prompts/{prompt_name}.txt")

    # Prepare the prompt
    prompt = read_and_fill_template(prompt_path, input_dict)
    if prompt is None:
        raise FileNotFoundError("Prompt file not found or failed to read.")

    # Communicate with GPT-4 and get the response
    responses = get_openai_responses([prompt], use_json=use_json)

    if use_json == False:
        return responses

    response_json = parse_json(responses[0])
    return response_json


# Test
if __name__ == "__main__":
    ckp1 = time.time()

    # TODO: Use pytest next time
    
    @dataclass
    class Job:
        job_position: str
        job_description: str
        previous_conversation: str
        

    job_position, job_description = "SWE Engineer", "Cadence: Currently pursuing MS degree in CE, EE, CS or equivalent with courses in design/verification using Verilog"
    previous_conversation = "  Interviewer: 'Can you give us a detailed example of a time when you led your team through a challenging project with a very tight deadline?' Candidate: Absolutely. Last year, I was leading a project aimed at developing a new encryption feature for our companys flagship messaging app, SecureTalk. The feature was critical for the next version release, scheduled for the end of Q2, to ensure compliance with new data protection regulations. We had exactly six weeks to go from concept to deployment, which was a significantly shorter timeline than usual for such a complex feature."
    
    user_input = Job(job_position=job_position, job_description=job_description, previous_conversation=previous_conversation)

    response = process_gpt_response(prompt_name = "amazon_interview", user_input=user_input, required_fields={})

    print(response[0])
