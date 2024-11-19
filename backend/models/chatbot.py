from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import Dict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Retrieve the Hugging Face access token from the environment
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")
print(f"Hugging Face Token Loaded: {HUGGING_FACE_TOKEN}")
# Device configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define model name
#MODEL_NAME = "openai-community/gpt2"  # Ensure correct model path
MODEL_NAME = "meta-llama/Llama-3.2-1B"  # Ensure correct model path

# Load the tokenizer and model with updated token parameter
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=HUGGING_FACE_TOKEN)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, token=HUGGING_FACE_TOKEN).to(device)

# Set `pad_token_id` to avoid warnings during generation
model.config.pad_token_id = model.config.eos_token_id

# Set `pad_token` as `eos_token` (or use add_special_tokens({'pad_token': '[PAD]'}))
tokenizer.pad_token = tokenizer.eos_token
model.resize_token_embeddings(len(tokenizer))

def process_prompt(prompt: str) -> str:
    """
    Generates a response to the given prompt using Llama 3.
    """
    try:
        # Ensure the prompt is a string
        if not isinstance(prompt, str):
            raise ValueError(f"Prompt must be a string. Received: {type(prompt)}")
        
        print(f"Processing prompt: {prompt}")

        # Tokenize and prepare attention mask
        inputs = tokenizer(prompt, return_tensors="pt", padding=True).to(device)

        # Generate response with attention_mask and pad_token_id
        outputs = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            pad_token_id=tokenizer.pad_token_id,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            max_new_tokens=3000  # Increase length limit
        )
        
        
        # Decode and return the generated response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    except Exception as e:
        print(f"Error processing prompt: {e}")
        return "There was an error generating a response."

# def handle_user_prompt(data: Dict) -> str:
#     """
#     Processes data received from the API endpoint and passes the prompt to the model.
#     """
#     prompt = data.get("prompt", "")
#     if not prompt:
#         return "Please provide a valid prompt."
    
#     return process_prompt(prompt)

# # Test prompt
# test_prompt = "What is the capital of France?"

# # Call the process_prompt function
# print("Processing prompt...")
# response = process_prompt(test_prompt)
# print("Response from model:")
# print(response)