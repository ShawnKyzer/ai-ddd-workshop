from kedro.pipeline import Pipeline, node
from .nodes import (
    setup_environment,
    create_tokenizer,
    prepare_data,
    create_model,
    create_peft_config,
    create_training_arguments,
    train_model
)

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=setup_environment,
                inputs=None,
                outputs=["compute_dtype", "attn_implementation"],
                name="setup_environment_node",
            ),
            node(
                func=create_tokenizer,
                inputs="params:model_name",
                outputs="tokenizer",
                name="create_tokenizer_node",
            ),
            node(
                func=prepare_data,
                inputs="data_with_prompts",
                outputs="prepared_dataset",
                name="prepare_data_node",
            ),
            node(
                func=create_model,
                inputs=["params:model_name", "compute_dtype", "attn_implementation"],
                outputs="model",
                name="create_model_node",
            ),
            node(
                func=create_peft_config,
                inputs=None,
                outputs="peft_config",
                name="create_peft_config_node",
            ),
            node(
                func=create_training_arguments,
                inputs=None,
                outputs="training_arguments",
                name="create_training_arguments_node",
            ),
            node(
                func=train_model,
                inputs=["model", "prepared_dataset", "peft_config", "tokenizer", "training_arguments"],
                outputs="trained_model",
                name="train_model_node",
            ),
        ]
    )