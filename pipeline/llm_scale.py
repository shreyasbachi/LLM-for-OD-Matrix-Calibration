import os
import timeit
import torch
import json
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM

# Change these paths as needed
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "config.json")
logs_path = os.path.join(PROJECT_ROOT, "logs")

HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")

# Model and tokenizer initialization
model_name = "meta-llama/Llama-3.3-70B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(
    model_name, 
    use_auth_token=HUGGING_FACE_API_KEY
)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype=torch.float16
)
model.eval()

def model_prompt():
    """
    Returns the system/user prompt for generating hourly scale factors.
    """
    prompt = """
You are a transportation modeling expert.
I have an origin-destination (OD) matrix representing total daily vehicle demand between zones.
I need to scale these values to estimate the number of vehicles per hour for each time interval between 5:00 AM and 11:00 PM.
Your task is to provide a realistic hourly distribution of traffic (as 19 fractional values that sum to 1) reflecting typical traffic patterns throughout the day. 
Assume a general urban setting with:
- a morning peak around 7–9 AM,
- a midday dip,
- and an evening peak around 4–6 PM.

Output a list of 19 fractional values corresponding to each hour slot, in order from 5:00 AM to 11:00 PM.

**Example Output Structure:**
{
    "5:00 AM": 0.0152,
    "6:00 AM": 0.0428,
    ...,
    "5:00 PM": 0.1214,
    "11:00 PM": 0.0081,
    "validation_sum": 1.0000
}

Also briefly explain the reasoning behind your distribution.
    """
    return prompt.strip()

def generate_output(prompt, model, tokenizer):
    """
    Runs the LLM to generate hourly scale factors, then saves and returns the text output.
    """
    # Time the generation
    start_time = timeit.default_timer()
    
    # Tokenize prompt
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    
    # Generate LLM output
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=2000,
            temperature=0.7,
            do_sample=True
        )
    
    # Decode to text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Ensure logs_path exists
    if not os.path.exists(logs_path):
        os.makedirs(logs_path, exist_ok=True)
        
    # Write output to a file
    output_path = os.path.join(logs_path, "llama_output_scale.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(generated_text)
    
    # Time taken
    end_time = timeit.default_timer()
    print(f"Time taken to generate output: {end_time - start_time:.2f} seconds")
    
    return generated_text

if __name__ == "__main__":
    prompt_text = model_prompt()
    llama_output = generate_output(prompt_text, model, tokenizer)
    print("LLM Output:")
    print(llama_output)
