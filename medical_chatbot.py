import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer


def main():
    # Load the fine-tuned model and tokenizer
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
        "You are an experienced medical doctor"
        "Provide a detailed and compassionate treatment plan to the patient's description based on the symptoms the patient describes."
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

        # conversation_history = []
        # while True:
        #     user_input = input("\nPatient: ")
        #     if user_input.lower() in ['exit', 'quit']:
        #         print("\nChatbot: Take care! Goodbye.")
        #         break

        #     # Append the user's input to the conversation history
        #     conversation_history.append(f"Patient's Description: {user_input}\n\nDoctor's Response:")

        #     # Keep only the last few exchanges to stay within model's max length
        #     conversation = "\n\n".join(conversation_history[-3:])

        #     # Prepare the prompt with conversation history
        #     prompt = f"{instruction}\n\n{conversation}"

        #     # Tokenize and generate as before
        #     inputs = tokenizer(prompt, return_tensors='pt').to(device)

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
            response = generated_text[
                response_start + len("Doctor's Response:") :
            ].strip()
        else:
            response = generated_text[len(prompt) :].strip()

        if response.startswith("Patient's Description:"):
            response = response.split("Patient's Description:")[0].strip()

        print(f"\nDoctor: {response}")


if __name__ == "__main__":
    main()
