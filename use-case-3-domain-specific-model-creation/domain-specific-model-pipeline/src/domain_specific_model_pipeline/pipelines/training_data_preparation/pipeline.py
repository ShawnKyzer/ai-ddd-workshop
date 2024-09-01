from kedro.pipeline import Pipeline, node
from .nodes import (
    extract_data_from_postgres,
    prepare_training_data,
    generate_prompts)

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=extract_data_from_postgres,
                inputs="experiments_table",
                outputs="raw_training_data",
                name="extract_data_from_postgres_node",
            ),
            node(
                func=prepare_training_data,
                inputs="raw_training_data",
                outputs="processed_training_data",
                name="prepare_training_data_node",
            ),
            node(
                func=generate_prompts,
                inputs=["processed_training_data", "params:llm_api"],
                outputs="data_with_prompts",
                name="generate_prompts_node",
            ),
        ]
    )