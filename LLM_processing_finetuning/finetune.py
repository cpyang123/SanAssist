import json
from datasets import Dataset
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
import torch
from peft import get_peft_model, LoraConfig
from transformers import default_data_collator


# 1. Load the distilgpt2 model and tokenizer
# tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')
# model = GPT2LMHeadModel.from_pretrained('distilgpt2')
# # Set the pad_token to eos_token
# tokenizer.pad_token = tokenizer.eos_token
# model.config.pad_token_id = tokenizer.eos_token_id


tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.add_special_tokens(
    {"eos_token": "<|endoftext|>", "pad_token": "<|endoftext|>"}
)

model = GPT2LMHeadModel.from_pretrained("gpt2")
model.resize_token_embeddings(len(tokenizer))
model.config.eos_token_id = tokenizer.eos_token_id
model.config.pad_token_id = tokenizer.pad_token_id

print("model loaded")

# 2. Apply LoRA
config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["c_attn", "c_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, config)
print("LoRA applied")
model.print_trainable_parameters()
print("trainable parameters printed")

# 3. Load and format your dataset (same as before)
# ... (use the same load_dataset function as earlier)
# def load_dataset(file_path):
#     with open(file_path, 'r') as file:
#         data = json.load(file)

#     # Limit to 1000 examples
#     data = data[:100]

#     formatted_data = []
#     for item in data:
#         instruction = item.get('instruction', '')
#         input_text = item.get('input', '')
#         output_text = item.get('output', '')

#         # Construct the prompt
#         if input_text:
#             prompt = f"{instruction}\n\nInput: {input_text}\n\nResponse:"
#         else:
#             prompt = f"{instruction}\n\nResponse:"

#         # Combine prompt and output
#         full_text = prompt + " " + output_text

#         formatted_data.append({'text': full_text})


#     return Dataset.from_dict({'text': [item['text'] for item in formatted_data]})
def load_dataset(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    data = data[:2000]  # 2k

    formatted_data = []
    for item in data:
        instruction = "You are an experienced medical doctor specializing in mental health. Provide a detailed and compassionate response to the patient's description."  # item.get('instruction', '')
        input_text = item.get("input", "")
        output_text = item.get("output", "")

        # Construct the prompt
        if input_text:
            prompt = f"{instruction}\n\nPatient's Description: {input_text}\n\nDoctor's Response"
        else:
            prompt = f"{instruction}\n\nDoctor's Response"

        formatted_data.append({"text": prompt, "label": output_text})

    return Dataset.from_dict(
        {
            "text": [item["text"] for item in formatted_data],
            "label": [item["label"] for item in formatted_data],
        }
    )


dataset = load_dataset("chatdoctor5k.json")  #'chatdoctor5k.json')

# 4. Tokenize the dataset
# def tokenize_function(examples):
#     return tokenizer(examples['text'], truncation=True, padding="longest", max_length=128 )


# tokenized_dataset = dataset.map(tokenize_function, batched=True)
def tokenize_function(examples):
    inputs = tokenizer(
        examples["text"], truncation=True, max_length=128, padding="longest"
    )
    outputs = tokenizer(
        examples["label"], truncation=True, max_length=128, padding="longest"
    )

    # Concatenate the inputs and outputs
    input_ids = []
    labels = []
    attention_masks = []
    for i in range(len(inputs["input_ids"])):
        input_id = inputs["input_ids"][i] + outputs["input_ids"][i]
        attention_mask = inputs["attention_mask"][i] + outputs["attention_mask"][i]
        label = [-100] * len(inputs["input_ids"][i]) + outputs["input_ids"][i]

        input_ids.append(input_id)
        attention_masks.append(attention_mask)
        labels.append(label)

    return {"input_ids": input_ids, "attention_mask": attention_masks, "labels": labels}


# tokenized_dataset = dataset.map(tokenize_function, batched=True)
tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=dataset.column_names,  # Remove original columns
)

# 5. Prepare data collator

data_collator = default_data_collator

# data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# 6. Set training arguments
training_args = TrainingArguments(
    output_dir="./lora_results",
    overwrite_output_dir=True,
    learning_rate=3e-4,
    per_device_train_batch_size=4,  # 4 or 8
    num_train_epochs=3,  # 3 or more
    logging_steps=10,
    save_steps=50,
    save_total_limit=2,
    remove_unused_columns=True,
    fp16=torch.cuda.is_available(),
    gradient_accumulation_steps=1,
    # evaluation_strategy="steps",
    # eval_steps=200,
)

# 7. Initialize trainer
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=tokenized_dataset,
)

# 8. Train the model
trainer.train()

# 9. Save the LoRA adapter
model.save_pretrained("./trained_lora_2k")
tokenizer.save_pretrained("./trained_lora_2k")
