from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments

# Load the model and tokenizer
model_name = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Load your dataset
from datasets import load_dataset
dataset = load_dataset("E:/GitHub/Artificial_Intelligence/YathzeeGameApp/train_data_yathzee.jsonl")
print(dataset)


# Tokenize the dataset
def preprocess_function(examples):
    return tokenizer(examples["inputs"], text_target=examples["outputs"], truncation=True)

tokenized_datasets = dataset.map(preprocess_function, batched=True)
print(tokenized_datasets)


# Set training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    num_train_epochs=3,
    weight_decay=0.01,
    save_steps=500,
    save_total_limit=2,
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
)
print(trainer)

# Train the model
trainer.train()
