import torch
import os
import multiprocessing
import json
from datasets import load_dataset, Dataset
from peft import LoraConfig, prepare_model_for_kbit_training, PeftConfig
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    set_seed
)
from trl import SFTTrainer, SFTConfig
from peft import PeftModel


def setup_environment():
    set_seed(1234)
    if torch.cuda.is_bf16_supported():
        os.system('pip install flash_attn')
        compute_dtype = torch.bfloat16
        attn_implementation = 'flash_attention_2'
    else:
        compute_dtype = torch.float16
        attn_implementation = 'sdpa'
    return compute_dtype, attn_implementation

def create_tokenizer(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    tokenizer.pad_token = "<|finetune_right_pad_id|>"
    tokenizer.pad_token_id = 128004
    tokenizer.padding_side = 'right'
    return tokenizer

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

def create_model(model_name, compute_dtype, attn_implementation):
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=compute_dtype,
        bnb_4bit_use_double_quant=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_name, quantization_config=bnb_config, device_map={"": 0}, attn_implementation=attn_implementation
    )
    model = prepare_model_for_kbit_training(model, gradient_checkpointing_kwargs={'use_reentrant': True})
    return model

def create_peft_config():
    return LoraConfig(
        lora_alpha=16,
        lora_dropout=0.05,
        r=16,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=['k_proj', 'q_proj', 'v_proj', 'o_proj', "gate_proj", "down_proj", "up_proj"]
    )

def create_training_arguments():
    return SFTConfig(
        output_dir="./Llama3.1_8b_QLoRA_right/",
        eval_strategy="steps",
        do_eval=True,
        optim="paged_adamw_8bit",
        per_device_train_batch_size=8,
        gradient_accumulation_steps=4,
        per_device_eval_batch_size=8,
        log_level="debug",
        save_strategy="epoch",
        logging_steps=25,
        learning_rate=1e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        eval_steps=25,
        num_train_epochs=1,
        warmup_ratio=0.1,
        lr_scheduler_type="linear",
        dataset_text_field="messages",
        max_seq_length=512,
    )

def train_model(model, dataset, peft_config, tokenizer, training_arguments):
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        eval_dataset=dataset,
        peft_config=peft_config,
        tokenizer=tokenizer,
        args=training_arguments,
    )
    trainer.train()
    
    # Get the trained PEFT model
    peft_model = trainer.model
    
    # Save the PEFT model and return the path
    adapter_path = "./peft_model"
    peft_model.save_pretrained(adapter_path)
    
    return adapter_path


def merge_and_push_model(model_name, adapter_path, compute_dtype, attn_implementation):
    # Load the base model
    base_model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        device_map="auto",
        trust_remote_code=True,
        torch_dtype=compute_dtype,
        attn_implementation=attn_implementation
    )
    
    # Load the PEFT model
    model = PeftModel.from_pretrained(base_model, adapter_path)
    
    # Merge and unload
    merged_model = model.merge_and_unload()
    
     # Load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Save the merged model and tokenizer
    output_dir = "./merged_model"
    merged_model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # Push both the model and tokenizer to the Hub
    merged_model_name = f"shawnkyzer/{model_name.split('/')[-1]}-merged"
    merged_model.push_to_hub(merged_model_name, use_auth_token=True)
    tokenizer.push_to_hub(merged_model_name, use_auth_token=True)
    
    return output_dir