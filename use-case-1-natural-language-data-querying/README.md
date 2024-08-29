# Use Case 1: NLQ-to-SQL Assistant

This directory demonstrates the first use case of our workshop: building an AI-powered SQL query assistant using Domain-Driven Design (DDD) principles. This assistant allows users to query a database using natural language.

## Overview

This use case leverages the following technologies:

* **Langflow:** A user interface for building and managing LLM workflows.
* **Langchain:** A framework for developing applications powered by language models.
* **Ollama:** A tool for running large language models locally.
* **Docker Compose:** For orchestrating the deployment and management of services.

## Getting Started

**Prerequisites:**

* Docker Desktop installed and running on your system. Installation instructions can be found [here](https://docs.docker.com/get-docker/)

**Steps:**

1. **Navigate to the use case directory:**
   ```bash
   cd use-case-1-natural-language-data-querying
   ```

2. **Start the services:**
   ```bash
   docker compose up -d
   ```

3. **Access Langflow:**
   Open your web browser and navigate to `http://localhost:7860`.

4. **Import the pipeline:**
   In Langflow, import the pipeline from `app_data/langflow/Example 1 - Natural Language Query to SQL.json`.

5. **Start querying:**
   Use the Langflow playground to input natural language queries and observe the generated SQL and results.

## Directory Structure

* **app_data/langflow:** Contains the Langflow pipeline definition.
* **docker-compose.yml:** Defines the services and their configurations for this use case.

## Learning Objectives

By completing this use case, you will:

1. Understand how to apply DDD principles to AI system design.
2. Learn to integrate language models with database querying.
3. Gain hands-on experience with Langflow and Langchain.
4. Practice implementing a practical AI-powered assistant.

## Next Steps

After completing this use case, you'll be ready to move on to Use Case 2: Data Extraction and Analysis. The skills you've learned here will provide a foundation for more advanced AI architecture design in the subsequent use cases.

## Acknowledgements

* **Langflow:** [https://github.com/logspace-ai/langflow](https://github.com/logspace-ai/langflow)
* **Langchain:** [https://github.com/hwchase17/langchain](https://github.com/hwchase17/langchain)
* **Ollama:** [https://github.com/jmorganca/ollama](https://github.com/jmorganca/ollama)

## Disclaimer

This project is part of a larger workshop and may undergo changes.

## Contact

For any questions or feedback specific to this use case, please contact the workshop organizers.