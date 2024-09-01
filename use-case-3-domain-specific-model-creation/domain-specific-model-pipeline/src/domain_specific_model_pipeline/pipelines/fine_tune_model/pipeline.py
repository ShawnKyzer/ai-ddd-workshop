from kedro.pipeline import Pipeline, node
from .nodes import prepare_data, setup_model_and_tokenizer, train_model, save_model

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=prepare_data,
                inputs="data_with_prompts",
                outputs="prepared_dataset",
                name="prepare_data_node",
            ),
            node(
                func=setup_model_and_tokenizer,
                inputs="params:model_name",
                outputs=["model", "tokenizer"],
                name="setup_model_and_tokenizer_node",
            ),
            node(
                func=train_model,
                inputs=["model", "tokenizer", "prepared_dataset", "prepared_dataset", "params:output_dir"],
                outputs="trained_model",
                name="train_model_node",
            ),
            node(
                func=save_model,
                inputs=["trained_model", "params:output_dir"],
                outputs=None,
                name="save_model_node",
            ),
        ]
    )