import torch
import json
from datasets import Dataset
from peft import LoraConfig, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTTrainer, SFTConfig

def prepare_data(data):
    # Convert the pandas DataFrame to a Hugging Face Dataset
    dataset = Dataset.from_pandas(data)
    
    # Create the messages column with system and user roles
    def process(example):
        messages = [
            {"role": "user", "content": example["generated_prompt"]},
            {"role": "assistant", "content": example["formatted_method"]}
        ]
        example["messages"] = json.dumps(messages)
        return example
    
    dataset = dataset.map(process)
    
    # Add the EOS token to each message
    def add_eos(example):
        example["messages"] = example["messages"] + "<|end_of_text|>"
        return example
    
    return dataset.map(add_eos)

def setup_model_and_tokenizer(model_name):
    # Set up tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    tokenizer.pad_token = "<|finetune_right_pad_id|>"
    tokenizer.pad_token_id = 128004
    tokenizer.padding_side = 'right'

    # Set up model with quantization
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        quantization_config=bnb_config, 
        device_map={"": 0}, 
        attn_implementation='flash_attention_2'
    )
    model = prepare_model_for_kbit_training(model)

    return model, tokenizer

def train_model(model, tokenizer, train_dataset, eval_dataset, output_dir):
    # Set up LoRA configuration
    peft_config = LoraConfig(
        lora_alpha=16,
        lora_dropout=0.05,
        r=16,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=['k_proj', 'q_proj', 'v_proj', 'o_proj', "gate_proj", "down_proj", "up_proj"]
    )

    # Set up training arguments
    training_arguments = SFTConfig(
        output_dir=output_dir,
        eval_strategy="steps",
        do_eval=True,
        optim="paged_adamw_8bit",
        per_device_train_batch_size=8,
        gradient_accumulation_steps=4,
        per_device_eval_batch_size=8,
        logging_steps=25,
        learning_rate=1e-4,
        bf16=True,
        eval_steps=25,
        num_train_epochs=1,
        warmup_ratio=0.1,
        lr_scheduler_type="linear",
        dataset_text_field="messages",
        max_seq_length=512,
    )

    # Set up trainer
    trainer = SFTTrainer(
        model=model,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        peft_config=peft_config,
        tokenizer=tokenizer,
        args=training_arguments,
    )

    # Train the model
    trainer.train()

    return trainer.model

def save_model(model, output_dir):
    model.save_pretrained(output_dir)