# from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer


# # Load your fine-tuned model and tokenizer

# model = AutoModelForSeq2SeqLM.from_pretrained("your_model_path")

# tokenizer = AutoTokenizer.from_pretrained("your_model_path")


# # Create a text generation pipeline

# pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)


# # Calculate perplexity on validation data

# def calculate_perplexity(text):

#     encoded_input = tokenizer(text, return_tensors="pt")

#     output = model.generate(**encoded_input)

#     log_probs = model(encoded_input, labels=output).loss.item()

#     perplexity = 2 ** log_probs

#     return perplexity


# # Example usage

# validation_text = "This is a sample sentence from our validation set."

# perplexity_score = calculate_perplexity(validation_text)

# print("Perplexity:", perplexity_score)


import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import json
import numpy as np


def calculate_perplexity(model, tokenizer, text, device):
    # Tokenize the entire text
    encodings = tokenizer(text, return_tensors="pt")

    # Get model's max sequence length
    max_length = model.config.max_position_embeddings
    stride = 512
    seq_len = encodings.input_ids.size(1)

    nll_sum = 0.0
    n_tokens = 0
    prev_end_loc = 0

    for begin_loc in range(0, seq_len, stride):
        end_loc = min(begin_loc + max_length, seq_len)
        trg_len = end_loc - prev_end_loc

        input_ids = encodings.input_ids[:, begin_loc:end_loc].to(device)
        target_ids = input_ids.clone()
        target_ids[:, :-trg_len] = -100

        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)
            neg_log_likelihood = outputs.loss

        # Calculate number of valid tokens
        num_valid_tokens = (target_ids != -100).sum().item()
        batch_size = target_ids.size(0)
        num_loss_tokens = num_valid_tokens - batch_size  # adjust for label shift

        nll_sum += neg_log_likelihood.item() * num_loss_tokens
        n_tokens += num_loss_tokens

        prev_end_loc = end_loc

        if end_loc == seq_len:
            break

    # Calculate average negative log-likelihood and perplexity
    avg_nll = nll_sum / n_tokens
    perplexity = torch.exp(torch.tensor(avg_nll)).item()

    return perplexity


def main(user_input):
    model_path = "./trained_lora_2k"
    tokenizer = GPT2Tokenizer.from_pretrained(model_path)
    model = GPT2LMHeadModel.from_pretrained(model_path)

    # Move model to the appropriate device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    if model.config.pad_token_id is None:
        model.config.pad_token_id = model.config.eos_token_id

    print(
        "Welcome to the Medical Chatbot. Type 'exit' or 'quit' to end the conversation."
    )
    instruction = (
        "You are an experienced medical doctor. "
        "Provide a detailed and compassionate treatment plan to the patient's description based on the symptoms the patient describes."
    )

    # Get user input
    # user_input = "Doctor, I recently had an ultrasound and they found a mass on my kidney. What could this mean?"
    # user_input = input("\nPatient: ")
    if user_input.lower() in ["exit", "quit"]:
        print("\nChatbot: Take care! Goodbye.")

    # Prepare the prompt
    prompt = (
        f"{instruction}\n\nPatient's Description: {user_input}\n\nDoctor's Response:"
    )

    # Tokenize the prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # Generate a response
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=True,
            temperature=0.8,
            top_p=0.5,
            repetition_penalty=1.01,
            no_repeat_ngram_size=4,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    response_start = generated_text.find("Doctor's Response:")
    if response_start != -1:
        response = generated_text[response_start + len("Doctor's Response:") :].strip()
    else:
        response = generated_text[len(prompt) :].strip()

    if response.startswith("Patient's Description:"):
        response = response.split("Patient's Description:")[0].strip()

    # Calculate and print perplexity
    perplexity = calculate_perplexity(model, tokenizer, response, device)
    print(f"\nGenerated Response: {response}")
    print(f"Perplexity: {perplexity:.2f}")

    return perplexity


if __name__ == "__main__":
    with open("chatdoctor5k.json", "r") as file:
        data = json.load(file)

    data = data[-50:]  # 2k

    perplexity_all = []
    for item in data:
        print(item)
        score = main(item.get("input", ""))
        perplexity_all.append(score)
        print(f"prompt: {item} and perplexity score: {score}")

    print("The perplexity calculated for the test set is:", np.mean(perplexity_all))
