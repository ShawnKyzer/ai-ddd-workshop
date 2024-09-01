import os
import pandas as pd
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def extract_data_from_postgres(experiments_table: pd.DataFrame) -> pd.DataFrame:
    raw_data = experiments_table.reset_index()[['id', 'extracted_method']]
    raw_data['extracted_method'] = raw_data['extracted_method'].astype(str)
    return raw_data

def prepare_training_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    def format_method(method):
        # This function should be adapted based on the structure of your extracted_method JSON
        # For this example, we'll assume it's a list of steps
        return "\n".join([f"Step {i+1}: {step}" for i, step in enumerate(method)])
    
    processed_data = raw_data.copy()
    processed_data['formatted_method'] = processed_data['extracted_method'] #.apply(format_method)
    return processed_data [['id', 'formatted_method']]


def generate_prompts(processed_data: pd.DataFrame, params: dict) -> pd.DataFrame:
    API_URL = params["url"]
    API_KEY = os.environ.get("LLM_API_TOKEN")

    # Define the prompt template
    prompt_template = """
You are an AI assistant specialized in formulating scientific questions or requests based on detailed experiment information. Your task is to take a structured description of an experiment and transform it into a natural language question or request that a scientist might ask, which would lead to this experiment being designed.

## Input Format
The input will be a JSON-like string containing the following keys:
- results
- objective
- procedure
- observations
- equipment_setup

## Output Format
Generate a natural language question or request that a scientist might ask, which would lead to the design of the experiment described in the input. The output should be a single string, phrased as a question or request.

## Instructions
1. Analyze the given experiment details, focusing on the objective and key aspects of the procedure.
2. Formulate a clear and concise question or request that encapsulates the main goal of the experiment.
3. Ensure the question or request is open-ended enough that it could lead to the design of the described experiment.
4. Use language that a scientist in the field would naturally use when asking for help or proposing an investigation.
5. Do not include specific details from the procedure or equipment setup unless they are crucial to understanding the core inquiry.

## Example
Input:
{{
  'results': 'The solution underwent a color change, indicating the successful synthesis of Gold Nanoparticles.',
  'objective': 'The main goal of the experiment was to synthesize Gold Nanoparticles using a method that involved heating a solution of Gold(III) chloride trihydrate and trisodium citrate dihydrate.',
  'procedure': [
    '1. Prepared 20 mL of 1 mM Gold(III) chloride trihydrate solution in a 50 mL beaker.',
    '2. Heated the solution to boiling while stirring.',
    '3. Rapidly added 2 mL of a 1% solution of trisodium citrate dihydrate.',
    '4. Continued heating and stirring until the solution turned deep red (about 10 minutes).',
    '5. Removed from heat and allowed to cool to room temperature.',
    '6. Performed UV-Vis spectroscopy to confirm nanoparticle formation.'
  ],
  'observations': 'Solution changed from pale yellow to colorless, then to dark purple, and finally to deep red.',
  'equipment_setup': 'Hot plate, magnetic stirrer, glassware, UV-Vis spectrometer were set up and used to prepare the solution, heat it, stir it, and confirm nanoparticle formation respectively.'
}}

Output:
"How can I synthesize Gold Nanoparticles using Gold(III) chloride trihydrate and trisodium citrate dihydrate? What procedure should I follow, and what observations should I expect during the process?"

Now, generate a scientific question or request based on the following experiment details, following the format and guidelines provided above:

{method}
"""

    def get_prompt(method):
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistral-tiny",
            "messages": [
                {"role": "system", "content": "You are an expert in formulating scientific questions based on experiment details."},
                {"role": "user", "content": prompt_template.format(method=json.dumps(method))}
            ]
        }
        response = requests.post(API_URL, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']

    processed_data['generated_prompt'] = processed_data['formatted_method'].apply(get_prompt)
    return processed_data