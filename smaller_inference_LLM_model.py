import openai
import json
import os

# Set your OpenAI API key securely
openai.api_key = "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" #os.getenv('OPENAI_API_KEY')  # Recommended to use environment variables

instruction = (
    "You are an experienced medical doctor. "
    "Provide a detailed and compassionate treatment plan to the patient's description "
    "based on the symptoms the patient describes, also consider the patient's known history "
    "from the provided database. "
    "Be sure to note any metrics that look concerning."
)

def generate_response_with_patient_data(user_input: str, patient_db: dict) -> str:
    """
    Generates a response from GPT-3.5-turbo given user input and patient database information.
    
    Args:
        user_input (str): The patient's description or query.
        patient_db (dict): A dictionary containing patient-specific data (e.g., name, history, known conditions).
        
    Returns:
        str: The doctor's response from the model.
    """
    # Convert the patient database to a readable string
    patient_db_str = json.dumps(patient_db, indent=2)
    
    # Prepare the prompt
    prompt = (
        f"{instruction}\n\n"
        f"Patient Database:\n{patient_db_str}\n\n"
        f"Patient's Concern: {user_input}\n\nDoctor's Response:"
    )
    
    # Call OpenAI's GPT-3.5-turbo API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": f"Patient Database:\n{patient_db_str}\n\nPatient's Concern: {user_input}"}
        ],
        max_tokens=500,
        temperature=0.8,
        top_p=0.5,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    
    # Extract the assistant's reply
    doctor_response = response.choices[0].message['content'].strip()
    
    return doctor_response

if __name__ == "__main__":
    # Example patient database
    patient_db_example = {
        "name": "John Doe",
        "age": 45,
        "known_conditions": ["hypertension", "type 2 diabetes"],
        "recent_tests": {
            "blood_pressure": "150/90 mmHg",
            "blood_sugar": "fasting glucose 140 mg/dL"
        }
    }
    
    # Example user input
    user_input = "Doctor, I recently had an ultrasound and they found a mass on my kidney. What could this mean?"
    
    # Generate and print the response
    response = generate_response_with_patient_data(user_input, patient_db_example)
    print("Doctor:", response)
