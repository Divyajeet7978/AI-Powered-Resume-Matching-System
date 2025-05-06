from transformers import BertForSequenceClassification, BertTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
import torch

def train():
    # Load and preprocess dataset
    dataset = load_dataset('your/resume-matching-dataset')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    
    def tokenize_function(examples):
        return tokenizer(
            examples['resume_text'],
            examples['job_description'],
            padding="max_length",
            truncation=True
        )
    
    tokenized_datasets = dataset.map(tokenize_function, batched=True)
    
    # Initialize model
    model = BertForSequenceClassification.from_pretrained(
        'bert-base-uncased',
        num_labels=1  # Regression task for similarity score
    )
    
    # Training configuration
    training_args = TrainingArguments(
        output_dir="./bert_model",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"]
    )
    
    trainer.train()
    trainer.save_model("./bert_model")
    tokenizer.save_pretrained("./bert_model")