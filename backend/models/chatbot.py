# chatbot.py
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import Dict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve the Hugging Face access token from the environment
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

# Define model name
MODEL_NAME = "meta-llama/Llama-3.2-1B"  # Replace with actual model path if it's locally stored or on Hugging Face

# Load the tokenizer and model with authentication
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_auth_token=HUGGING_FACE_TOKEN)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, use_auth_token=HUGGING_FACE_TOKEN)

def process_prompt(prompt: str) -> str:
    """
    Generates a response to the given prompt using Llama 3.
    """
    try:
        # Tokenize the prompt and generate a response
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(inputs["input_ids"], max_length=150)
        
        # Decode the generated tokens
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    except Exception as e:
        print(f"Error processing prompt: {e}")
        return "There was an error generating a response."

def handle_user_prompt(data: Dict) -> str:
    """
    Wrapper function that processes data received from the API endpoint
    and passes the prompt to the model.
    """
    prompt = data.get("prompt", "")
    if not prompt:
        return "Please provide a valid prompt."
    
    # Process the prompt and return the response
    return process_prompt(prompt)
