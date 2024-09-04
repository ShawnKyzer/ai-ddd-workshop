import json
import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional

load_dotenv()

LLM_API_URL = os.getenv('LLM_API_URL')
LLM_API_TOKEN = os.getenv('LLM_API_TOKEN')
LLM_MODEL = os.getenv('LLM_MODEL')  # Default to 'mistral:7b' if not set

import logging
import requests
from typing import Optional, Dict, Any

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def call_llm(prompt: str, max_attempts: int = 2) -> Optional[Dict[str, Any]]:
    headers = {
        "Authorization": f"Bearer {LLM_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    for attempt in range(max_attempts):
        try:
            response = requests.post(LLM_API_URL, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Attempt {attempt + 1}: Error occurred - {str(e)}")
            logger.debug(f"Request payload: {data}")
            logger.debug(f"Response content: {response.text}")
            if attempt == max_attempts - 1:
                logger.error("All attempts failed")
                return None
    
    return None

def generate_experiment(input_text: str, rule_guidance: str = "") -> Optional[Dict[str, Any]]:
    prompt = f"""
    Generate a detailed experiment based on the following input and guidance:

    Input: {input_text}
    Guidance: {rule_guidance}

    Please provide a structured JSON output with the following fields:
    1. objective: The main goal of the experiment
    2. equipment_setup: Description of how the equipment should be set up
    3. procedure: Detailed step-by-step procedure
    4. observations: Expected key observations during the experiment
    5. results: Anticipated results or conclusions

    Output the result as a valid JSON object.
    """
    
    response = call_llm(prompt)
    if response and 'choices' in response:
        try:
            # The LLM response is already parsed into a dictionary
            # We need to extract the content from the message
            content = response['choices'][0]['message']['content']
            # Now parse this content as JSON
            return json.loads(content)
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error: Failed to parse LLM response as JSON: {e}")
            return None
    return None
def llm_self_reflection(experiment: Dict[str, Any], evaluation: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    prompt = f"""
    Provide a reflective analysis of the following experiment and its evaluation:

    Experiment:
    {json.dumps(experiment, indent=2)}

    Evaluation:
    {json.dumps(evaluation, indent=2)}

    Please provide a structured JSON output with the following fields:
    1. strengths: Key strengths of the experiment
    2. weaknesses: Areas that need improvement
    3. suggestions: Specific suggestions for enhancing the experiment
    4. overall_assessment: A brief overall assessment of the experiment quality

    Output the result as a valid JSON object.
    """
    
    response = call_llm(prompt)
    if response and 'choices' in response:
        try:
            content = response['choices'][0]['message']['content']
            return json.loads(content)
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error: Failed to parse LLM response as JSON: {e}")
            return None
    return None
# Example usage:
# experiment = generate_experiment("Investigate the effect of temperature on enzyme activity", "Focus on a specific enzyme")
# if experiment:
#     print("Generated Experiment:")
#     print(json.dumps(experiment, indent=2))
#
#     evaluation = {"accuracy": 8, "completeness": 7, "feasibility": 9}
#     reflection = llm_self_reflection(experiment, evaluation)
#     if reflection:
#         print("\nReflection:")
#         print(json.dumps(reflection, indent=2))
# else:
#     print("Failed to generate experiment")