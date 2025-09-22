import os
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from peft import get_peft_model, LoraConfig, TaskType

def train_real_lora_model(data_path: str, base_model: str, run_id: str) -> str:
    """
    Trains a real LoRA model on the fetched text data for sequence classification.
    """
    print(f"--- STARTING REAL LoRA TRAINING for run {run_id} ---")
    
    dataset = load_dataset("text", data_files=data_path, split='train')
    
    def add_labels(example, idx):
        example['label'] = idx % 2
        return example
    dataset = dataset.map(add_labels, with_indices=True)

    tokenizer = AutoTokenizer.from_pretrained(base_model)
    def preprocess_function(examples):
        return tokenizer(examples['text'], truncation=True, padding='max_length', max_length=128)
    
    tokenized_dataset = dataset.map(preprocess_function, batched=True)
    tokenized_dataset = tokenized_dataset.train_test_split(test_size=0.1)

    model = AutoModelForSequenceClassification.from_pretrained(base_model, num_labels=2)
    
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_lin", "v_lin"], # This line fixes the error
        lora_dropout=0.1,
        bias="none",
        task_type=TaskType.SEQ_CLS
    )
    peft_model = get_peft_model(model, lora_config)
    peft_model.print_trainable_parameters()

    output_dir = f"outputs/{run_id}"
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=8,
        num_train_epochs=1,
        logging_steps=10,
        save_strategy="epoch",
        eval_strategy="epoch",
        learning_rate=2e-5,
        weight_decay=0.01,
        load_best_model_at_end=True,
        use_cpu=True
    )

    trainer = Trainer(
        model=peft_model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["test"],
    )

    print("Starting training...")
    trainer.train()
    
    print(f"Training complete. Saving model to {output_dir}")
    trainer.save_model(output_dir)
    return output_dir