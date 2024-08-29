# NLQ-to-SQL Assistant

This repository demonstrates a practical application of Domain-Driven Design (DDD) principles to build an AI-powered SQL query assistant. This assistant allows users to query a database using natural language. Please read original blog post [here](https://opendatascience.com/domain-driven-design-in-practice-crafting-an-ai-assistant-step-by-step/) for more information. 

## Overview

This project leverages the following technologies:

* **Langflow:** A user interface for building and managing LLM workflows.
* **Langchain:** A framework for developing applications powered by language models.
* **Ollama:** A tool for running large language models locally.
* **Docker Compose:** For orchestrating the deployment and management of services.

## Getting Started

**Prerequisites:**

* Docker Desktop installed and running on your system. Installion instructions can be found [here](https://docs.docker.com/get-docker/)

**Steps:**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ShawnKyzer/nlq-to-sql-assistant.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd nlq-to-sql-assistant
   ```

3. **Start the services:**
   ```bash
   docker compose up -d
   ```

4. **Access Langflow:**
   Open your web browser and navigate to `http://localhost:7860`.

5. **Import the pipeline:**
   In Langflow, import the pipeline from `app_data/langflow/Example 1 - Natural Language Query to SQL.json`.

6. **Start querying:**
   Use the Langflow playground to input natural language queries and observe the generated SQL and results.

## Project Structure

* **app_data/langflow:** Contains the Langflow pipeline definition.
* **docker-compose.yml:** Defines the services and their configurations.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.


## Acknowledgements

* **Langflow:** [https://github.com/logspace-ai/langflow](https://github.com/logspace-ai/langflow)
* **Langchain:** [https://github.com/hwchase17/langchain](https://github.com/hwchase17/langchain)
* **Ollama:** [https://github.com/jmorganca/ollama](https://github.com/jmorganca/ollama)

## Disclaimer

This project is currently in development and may undergo changes.

## Contact

For any questions or feedback, please contact Shawn Kyzer at [shawnkyzer@gmail.com](mailto:shawnkyzer@gmail.com).
