import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer


def main():
    # Load the base GPT-2 model and tokenizer
    model_name = "gpt2"  # You can also try 'gpt2-medium', 'gpt2-large', etc.
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Move model to the appropriate device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    # Set special tokens if not already set
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    if model.config.pad_token_id is None:
        model.config.pad_token_id = model.config.eos_token_id

    # Welcome message
    print(
        "Welcome to the GPT-2 Chatbot. Type 'exit' or 'quit' to end the conversation."
    )

    # Define the instruction (same as in your fine-tuned model for consistency)
    instruction = (
        "You are an experienced medical doctor"
        "Provide a detailed and compassionate response to the patient's description."
    )

    while True:
        # Get user input
        user_input = input("\nPatient: ")
        if user_input.lower() in ["exit", "quit"]:
            print("\nChatbot: Take care! Goodbye.")
            break

        # Prepare the prompt
        prompt = f"{instruction}\n\nPatient's Description: {user_input}\n\nDoctor's Response:"

        # Tokenize the prompt
        inputs = tokenizer(prompt, return_tensors="pt").to(device)

        # Generate a response
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=200,
                do_sample=True,
                temperature=0.7,
                top_p=0.8,
                pad_token_id=tokenizer.eos_token_id,
            )

        # Decode the generated tokens
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract the doctor's response
        response_start = generated_text.find("Doctor's Response:")
        if response_start != -1:
            response = generated_text[
                response_start + len("Doctor's Response:") :
            ].strip()
        else:
            response = generated_text[len(prompt) :].strip()

        # Handle cases where the model includes the prompt in the output
        if response.startswith("Patient's Description:"):
            response = response.split("Patient's Description:")[0].strip()

        # Print the response
        print(f"\nDoctor: {response}")


if __name__ == "__main__":
    main()
