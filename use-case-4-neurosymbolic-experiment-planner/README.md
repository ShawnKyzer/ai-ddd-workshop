# AI-Powered Experiment Generator 🧪🤖

<p align="center">
  <a href="https://experiment-planner.streamlit.app/" target="_blank">
    <img src="https://img.shields.io/badge/Try%20Demo-🧬%20🔬%20🧫-blue?style=for-the-badge" alt="Try Demo" >
  </a>
</p>

Click the button above to try our interactive AI Experiment Generator demo!

This project implements an AI-driven system for generating, evaluating, and refining scientific experiments. It uses a combination of Large Language Models (LLMs), a graph database (Neo4j), and custom evaluation logic to create and improve experimental designs.

## Features 🌟

- 🧠 Generate experiment designs based on user input and historical data
- ✅ Evaluate experiments using predefined rules
- 💾 Store experiments and their evaluations in a Neo4j graph database
- 🤔 Generate self-reflections on experiment quality
- 📊 Produce HTML reports of generated experiments and best historical experiments
- 🖥️ Interactive demo application built with Streamlit

## Project Structure 📁

```
.
├── src/
│   ├── main.py
│   ├── database.py
│   ├── evaluator.py
│   ├── llm_interface.py
│   └── html_generator.py
├── docker-compose.yml
├── neo4j_setup.cypher
├── requirements.txt
└── README.md
```

## Components 🧩

1. `src/main.py`: The entry point of the application, orchestrating the experiment generation and evaluation process.
2. `src/database.py`: Handles interactions with the Neo4j graph database.
3. `src/evaluator.py`: Implements the `ExperimentEvaluator` class for assessing experiments.
4. `src/llm_interface.py`: Manages communications with the Large Language Model API.
5. `src/html_generator.py`: Generates HTML reports.
6. `neo4j_setup.cypher`: Contains Cypher queries for setting up the Neo4j database schema.
7. `docker-compose.yml`: Defines the Docker services for Neo4j and Ollama.

## Setup 🛠️

1. Install Docker and Docker Compose on your system.

2. Clone this repository and navigate to the project directory.

3. Create a `.env` file in the project root with the following variables:
   ```
   NEO4J_URI=bolt://neo4j:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=
   LLM_API_URL=http://ollama:11434/api/generate
   LLM_API_TOKEN=
   LLM_MODEL=llama3.1:latest
   ```

4. Start the Docker services:
   ```
   docker-compose up -d
   ```

5. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

6. Initialize the Neo4j database:
   - Open the Neo4j browser at `http://localhost:7474`
   - Copy the contents of `neo4j_setup.cypher` and run them in the Neo4j browser to set up the schema and initial data.

## Usage 🚀

Run the main script to start the experiment generation process:

```
python src/main.py
```

The script will prompt you for an experiment description. It will then generate multiple variants, evaluate them, and store the results in the Neo4j database. Finally, it will display the best experiments and generate an HTML report.

## Docker Services 🐳

This project uses Docker to run Neo4j and Ollama services:

- Neo4j: A graph database used to store experiment data and rules.
- Ollama: A service for running large language models locally.

The `docker-compose.yml` file defines these services and their configurations.

## Demo Application 🖥️

We've created an interactive demo application using Streamlit to showcase the capabilities of our AI-Powered Experiment Generator. You can access it by clicking the "Try Demo" button at the top of this README. The demo allows you to:

- 📝 Input experiment descriptions
- 🔬 Generate and view experiment designs
- 📊 See evaluations and reflections on the generated experiments
- 🏆 Explore the best historical experiments from our database

Try it out to get a hands-on feel for how our system works!

## Extending the Project 🔧

- Implement additional evaluation rules in `src/evaluator.py`
- Enhance the LLM prompts in `src/llm_interface.py` for better experiment generation and reflection
- Add more sophisticated querying and analysis of historical experiments in `src/database.py`
- Modify the `src/html_generator.py` file to create more detailed reports of the experiments
- Expand the Streamlit demo application with more features and visualizations

## Contributing 🤝

Contributions to improve the project are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License 📄

[Insert your chosen license here]