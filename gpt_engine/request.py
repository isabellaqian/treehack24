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
    input_dict = asdict(user_input)
    current_dir = os.path.abspath(os.path.dirname(__file__))
    prompt_path = os.path.join(current_dir, f"prompts/{prompt_name}.txt")

    # Prepare the prompt
    prompt = read_and_fill_template(prompt_path, input_dict)
    if prompt is None:
        raise FileNotFoundError("Prompt file not found or failed to read.")

    print(prompt)

    # Communicate with GPT-4 and get the response
    responses = get_openai_responses([prompt], use_json=use_json)

    if use_json == False:
        print(responses)
        return responses[0]

    response_json = parse_json(responses[0])

    if response_json is None:
        raise ValueError("GPT-4 response was not valid JSON.")

    # Validate and return the response
    if not validate_json_fields(response_json, required_fields):
        raise ValueError("GPT-4 response didn't contain the required fields.")

    return response_json


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
    responses = get_openai_responses([prompt])

    if use_json == False:
        return responses

    response_json = parse_json(responses[0])
    return response_json


# Test
if __name__ == "__main__":
    ckp1 = time.time()

    # TODO: Use pytest next time

    """

    @dataclass
    class Usercase:
        content: str

    case_input = "原告：覃小明（未成年）被告：邓丽华（其母）案由：共有纠纷-共有物分割纠纷案情：覃小明的父亲在2017年12月21日因一次工地意外去世，留下了年幼的覃小明和母亲邓丽华。这个悲剧震惊了整个家庭，也让覃小明的外祖母承担了实际抚养孙子的责任。覃小明的母亲邓丽华，虽然因为这次悲剧获得了620000元的经济赔偿，却因为种种原因未尽抚养义务。这笔赔偿款并没有直接存入覃小明或邓丽华的名下。事实上，邓丽华担心自己会不合理支配这笔款项，因此与覃小明的姨妈李秀芬商量后，决定存入李秀芬名下，希望她能帮忙管理。李秀芬对此事犹豫了一下，最终还是在2018年3月15日答应了。她知道邓丽华的性格冲动，对金钱管理也不够理智。于是，这笔钱在2018年4月10日存入了李秀芬名下的银行账户。不过，随着时间的推移，事情逐渐变得复杂。邓丽华在2018年至2019年期间多次向李秀芬提取资金，总计领取了205039元。而李秀芬也以出具借条的方式，实际支配了300000元，这让覃小明感到非常不满。几年过去，覃小明渐渐长大，开始关心自己的权益。他对母亲未尽抚养义务和赔偿款被不当支配的情况深感不满。通过外祖母和一些亲戚的了解，他对整个事件有了更清晰的认识。终于，到了2022年6月1日，覃小明下定决心，决定采取法律手段来解决这个问题。他聘请了律师，将母亲邓丽华告上法庭，诉请法院判决她赔偿共有款项400000元。"
    user_input = Usercase(content=case_input)
    required_output = {"question_1", "question_2", "question_3", "question_4", "outline", "features"}

    response = process_gpt_response(prompt_name = "case_input", user_input=user_input, required_fields=required_output)
    print(response["features"])

    user_inputs = [Usercase(content=case_input), Usercase(content=case_input)]

    responses = parallel_request(prompt_name = "case_input", user_inputs=user_inputs)

    print(responses)
    
    @dataclass
    class Supplement:
        outline: str
        init: str
        q1: str
        q2: str
        q3: str
        q4: str

    required_output = {"updated_features", "conflict_focus", "updated_outline", "detailed_summary"}

    user_input = Supplement(outline=response["outline"], init="features", q1="丽华与李秀芬之间存款协议的具体内容，是否形成了书面协议，或者有无可信的口头协议证人。", q2="邓丽华虽然担心自己管理不善，但将钱存入李秀芬名下，未设置监督机制，缺乏法律意识。", q3="偿金的法律地位及其应有的合理使用范围，是否所有支出都应与覃小明的利益直接相关。", q4="对于覃小明的实际生活状况，学习环境进行全面了解，评估未尽监护责任给他的成长带来的实际影响。")
    response = process_gpt_response(prompt_name = "case_input_sup", user_input=user_input, required_fields=required_output)
    print(response)
    
    ckp2 = time.time()
    print(f"Time is {ckp2 - ckp1}")
    """
