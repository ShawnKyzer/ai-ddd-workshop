import os
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
import psycopg2
from psycopg2.extras import DictCursor
import requests
import json

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data_from_postgres():
    conn = psycopg2.connect(
        dbname=os.environ.get("POSTGRES_DB"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("POSTGRES_HOST"),
        port=os.environ.get("POSTGRES_PORT")
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        SELECT id, experiment_name, researcher, date_conducted, 
               equipment_used, reagents, temperature, pressure, 
               duration, notes
        FROM experiments
        WHERE extracted_method IS NULL
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@task
def extract_experiment_method(experiment):
    prompt = f"""
    Extract the detailed experiment method from the following experiment information:

    Experiment Name: {experiment['experiment_name']}
    Researcher: {experiment['researcher']}
    Date Conducted: {experiment['date_conducted']}
    Equipment Used: {', '.join(experiment['equipment_used'])}
    Reagents: {json.dumps(experiment['reagents'])}
    Temperature: {experiment['temperature']}°C
    Pressure: {experiment['pressure']} kPa
    Duration: {experiment['duration']}
    Notes: {experiment['notes']}

    Please provide a structured JSON output with the following fields:
    1. objective: The main goal of the experiment
    2. equipment_setup: Description of how the equipment was set up
    3. procedure: Detailed step-by-step procedure
    4. observations: Key observations made during the experiment
    5. results: Any results or conclusions drawn

    Output the result as a valid JSON object.
    """
    
    for attempt in range(2):  # Try twice
        try:
            response = requests.post(
                "http://ollama:11434/api/generate",
                json={
                    "model": "mistral:7b",
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            response.raise_for_status()  # Raise an exception for bad status codes
            result = response.json()
            
            if 'response' not in result:
                print(f"Attempt {attempt + 1}: Unexpected API response format")
                if attempt == 1:  # If this is the second attempt, return None
                    return None
                continue  # Try again if it's the first attempt
            
            extracted_data = json.loads(result['response'])
            return extracted_data
        
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"Attempt {attempt + 1}: Error occurred - {str(e)}")
            if attempt == 1:  # If this is the second attempt, return None
                return None
    
    return None  # If we get here, both attempts failed
@task
def save_extracted_data(experiment_id, extracted_method):
    conn = psycopg2.connect(
        dbname=os.environ.get("POSTGRES_DB"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("POSTGRES_HOST"),
        port=os.environ.get("POSTGRES_PORT")
    )
    cur = conn.cursor()
    cur.execute(
        "UPDATE experiments SET extracted_method = %s WHERE id = %s",
        (json.dumps(extracted_method), experiment_id)
    )
    conn.commit()
    cur.close()
    conn.close()

@flow
def extract_and_save_experiment_methods():
    experiments = extract_data_from_postgres()
    for experiment in experiments:
        extracted_method = extract_experiment_method(experiment)
        save_extracted_data(experiment['id'], extracted_method)

if __name__ == "__main__":
    extract_and_save_experiment_methods()