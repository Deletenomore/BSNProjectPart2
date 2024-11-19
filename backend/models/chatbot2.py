from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve Hugging Face token
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")
if not HUGGING_FACE_TOKEN:
    raise ValueError("Hugging Face Token is not set in the environment variables.")
print(f"Hugging Face Token Loaded: {HUGGING_FACE_TOKEN}")

# Device configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define model name
MODEL_NAME = "openai-community/gpt2"  # Replace with the correct model name
print(f"Loading model: {MODEL_NAME}")

# Load tokenizer and model
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_auth_token=HUGGING_FACE_TOKEN)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, use_auth_token=HUGGING_FACE_TOKEN).to(device)
except Exception as e:
    raise ValueError(f"Failed to load model or tokenizer: {e}")

# Configure tokenizer and model
tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = model.config.eos_token_id

def process_prompt(prompt: str, max_length: int = 200, temperature: float = 0.7) -> str:
    """
    Generates a response to the given prompt using the Hugging Face model.
    """
    try:
        print(f"Received prompt: {prompt}")
        inputs = tokenizer(prompt, return_tensors="pt", padding=True).to(device)

        # Generate response
        outputs = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=max_length,
            temperature=temperature,
            pad_token_id=tokenizer.pad_token_id,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            max_new_tokens=3000  # Increase length limit
        )

        # Decode and return the response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Generated response: {response}")
        return response

    except Exception as e:
        print(f"Error generating response: {e}")
        return "An error occurred while generating the response."

# Test the implementation
if __name__ == "__main__":
    test_prompt = "What is the capital of France?"
    print("Processing prompt...")
    response = process_prompt(test_prompt)
    print("Response:")
    print(response)
