# # Use a pipeline as a high-level helper
# from transformers import pipeline

# # messages = [
# #     {"role": "user", "content": "Who are you?"},
# # ]
# # pipe = pipeline("text-generation", model="m42-health/Llama3-Med42-8B")
# # pipe(messages)

# # # Load model directly
# # from transformers import AutoTokenizer, AutoModelForCausalLM

# # tokenizer = AutoTokenizer.from_pretrained("m42-health/Llama3-Med42-8B")
# # model = AutoModelForCausalLM.from_pretrained("m42-health/Llama3-Med42-8B")


# from transformers import pipeline

# # Initialize the pipeline with the desired model
# pipe = pipeline("text-generation", model="m42-health/Llama3-Med42-8B", device_map="auto")

# def get_treatment_plan(patient_data: str, user_query: str) -> str:
#     """
#     Given patient data and a user query, use the pipeline to produce
#     a medical treatment plan or address the query as if you're a doctor.
#     """
#     # Construct a prompt that provides context and the user's question
#     prompt = (
#         f"Below is medical information about a patient:\n{patient_data}\n\n"
#         f"The user has the following question:\n{user_query}\n\n"
#         "As a qualified medical doctor, please provide the best possible treatment plan or answer the query."
#     )

#     # Generate the response using the pipeline
#     outputs = pipe(
#         prompt, 
#         max_length=512,  # Adjust as needed
#         num_return_sequences=1, 
#         do_sample=False
#     )

#     # The pipeline returns a list of generated sequences. Extract the text.
#     response = outputs[0]['generated_text']



#     return response


# if __name__ == "__main__":
#     patient_data_example = "Patient is a 45-year-old male with hypertension and type 2 diabetes."
#     user_query_example = "What medication should he be taking?"
#     answer = get_treatment_plan(patient_data_example, user_query_example)
#     print("Doctor's Response:", answer)


# import transformers
# import torch

# model_name_or_path = "m42-health/Llama3-Med42-8B"

# pipeline = transformers.pipeline(
#     "text-generation",
#     model=model_name_or_path,
#     torch_dtype=torch.bfloat16,
#     device_map="auto",
# )

# messages = [
#     {
#         "role": "system",
#         "content": (
#             "You are a helpful, respectful and honest medical assistant. You are a second version of Med42 developed by the AI team at M42, UAE. "
#             "Always answer as helpfully as possible, while being safe. "
#             "Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. "
#             "Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. "
#             "If you don’t know the answer to a question, please don’t share false information."
#         ),
#     },
#     {"role": "user", "content": "What are the symptoms of diabetes?"},
# ]

# prompt = pipeline.tokenizer.apply_chat_template(
#     messages, tokenize=False, add_generation_prompt=False
# )

# stop_tokens = [
#     pipeline.tokenizer.eos_token_id,
#     pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
# ]

# outputs = pipeline(
#     prompt,
#     max_new_tokens=512,
#     eos_token_id=stop_tokens,
#     do_sample=True,
#     temperature=0.4,
#     top_k=150,
#     top_p=0.75,
# )

# print(outputs[0]["generated_text"][len(prompt) :])




from transformers import pipeline

# Try a simpler call first to see if the model returns anything at all
pipe = pipeline("text-generation", model="m42-health/Llama3-Med42-8B", device_map="auto")

def get_treatment_plan(patient_data: str, user_query: str) -> str:
    # A simpler prompt, directly asking the model:
    prompt = (
        f"Patient data: {patient_data}\n\n"
        f"Question: {user_query}\n\n"
        "As a qualified medical doctor, provide the best possible treatment plan or answer.\n"
    )

    outputs = pipe(
        prompt,
        max_new_tokens=200,       # Limit how much text we generate
        do_sample=False,
        truncation=True           # Explicitly enable truncation
    )
    
    # Get the raw response (the model may or may not repeat the prompt)
    raw_response = outputs[0]['generated_text']
    
    # Print raw response for debugging
    print("Raw Response:", repr(raw_response))
    
    # If the model is repeating the prompt, you can try removing it.
    # But first, check what the raw response looks like.
    # If needed, remove the prompt prefix only if it appears at the start.
    if raw_response.startswith(prompt):
        response = raw_response[len(prompt):].strip()
    else:
        response = raw_response.strip()

    return response

if __name__ == "__main__":
    patient_data_example = "A 45-year-old male with hypertension and type 2 diabetes."
    user_query_example = "What medication should he be taking?"
    answer = get_treatment_plan(patient_data_example, user_query_example)
    print("Doctor's Response:", answer)
