# ELN Data Extraction Pipeline

This project implements a data extraction pipeline for Electronic Lab Notebooks (ELNs) using Prefect, PostgreSQL, and Ollama.

## Setup

1. Ensure Docker and Docker Compose are installed on your system.
2. Run the following command to start the services:

   ```
   docker-compose up --build
   ```

3. The pipeline will automatically start extracting data from the PostgreSQL database, process it using Ollama, and save the results back to the database.

## Project Structure

- `src/`: Contains the Python source code
- `config/`: Contains configuration files
- `docker/`: Contains Docker-related files
- `data/`: Directory for any additional data files
- `docker-compose.yml`: Defines and configures the Docker services
- `requirements.txt`: Lists the Python dependencies

## Customization

You can modify the `src/main.py` file to customize the data extraction logic or add additional processing steps.
