import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import json

# Load the model and tokenizer once at the start 
model_path = './trained_lora_2k'
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
model.eval()

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
if model.config.pad_token_id is None:
    model.config.pad_token_id = model.config.eos_token_id

instruction = (
    "You are an experienced medical doctor. "
    "Provide a detailed and compassionate treatment plan to the patient's description "
    "based on the symptoms the patient describes, also consider the patient's known history "
    "from the provided database."
)

def generate_response_with_patient_data(user_input: str, patient_db: dict) -> str:
    """
    Generates a response from the model given user input and patient database information.
    
    Args:
        user_input (str): The patient's description or query.
        patient_db (dict): A dictionary containing patient-specific data (e.g. name, history, known conditions).
        
    Returns:
        str: The doctor's response from the model.
    """
    # Convert the patient database to a string (e.g., JSON format)
    patient_db_str = json.dumps(patient_db, indent=2)

    # Incorporate patient DB info into the prompt
    prompt = (
        f"{instruction}\n\n"
        f"Patient Database:\n{patient_db_str}\n\n"
        f"Patient's Description: {user_input}\n\nDoctor's Response:"
    )

    # Tokenize the prompt
    inputs = tokenizer(prompt, return_tensors='pt').to(device)

    # Generate model output
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

    # Extract the doctor's response
    response_start = generated_text.find("Doctor's Response:")
    if response_start != -1:
        response = generated_text[response_start + len("Doctor's Response:"):].strip()
    else:
        response = generated_text[len(prompt):].strip()

    # If the model tries to mention "Patient's Description:" again, remove it
    if response.startswith("Patient's Description:"):
        response = response.split("Patient's Description:")[0].strip()

    return response

if __name__ == "__main__":

    patient_db_example = {
        "name": "John Doe",
        "age": 45,
        "known_conditions": ["hypertension", "type 2 diabetes"],
        "recent_tests": {
            "blood_pressure": "150/90 mmHg",
            "blood_sugar": " fasting glucose 140 mg/dL"
        }
    }

    user_input = "Doctor, I recently had an ultrasound and they found a mass on my kidney. What could this mean?"
    response = generate_response_with_patient_data(user_input, patient_db_example)
    print("Doctor:", response)
