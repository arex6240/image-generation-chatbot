import os
import requests
import io
import urllib.parse
from PIL import Image
import dotenv

# Load environment variables from .env file if it exists
dotenv.load_dotenv()

# API configuration keys
HF_API_KEY_ENV = "HUGGINGFACE_API_KEY"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"

def get_api_key(provider):
    """
    Retrieves the API key for the given provider.
    Checks Streamlit secrets first, then falls back to environment variables.
    """
    # Streamlit imports are kept dynamic so the module remains importable outside streamlit
    try:
        import streamlit as st
        # Check Streamlit secrets
        if provider == "huggingface" and HF_API_KEY_ENV in st.secrets:
            return st.secrets[HF_API_KEY_ENV]
        elif provider == "openai" and OPENAI_API_KEY_ENV in st.secrets:
            return st.secrets[OPENAI_API_KEY_ENV]
    except Exception:
        pass
    
    # Fallback to environment variables
    if provider == "huggingface":
        return os.environ.get(HF_API_KEY_ENV) or os.environ.get("HF_TOKEN")
    elif provider == "openai":
        return os.environ.get(OPENAI_API_KEY_ENV)
        
    return None

def generate_image_pollinations(prompt, size="1024x1024", negative_prompt=None, seed=None):
    """
    Generates an image using Pollinations.ai (Free, no API key required).
    """
    # Parse width and height from size string (e.g. "1024x1024" -> 1024, 1024)
    try:
        width, height = map(int, size.split('x'))
    except ValueError:
        width, height = 1024, 1024
        
    # Build prompt and parameters
    encoded_prompt = urllib.parse.quote(prompt)
    
    # Pollinations supports model parameter (flux, turbo, etc.)
    # flux is standard and yields fantastic results
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&nologo=true"
    
    if negative_prompt:
        url += f"&negative={urllib.parse.quote(negative_prompt)}"
    if seed is not None:
        url += f"&seed={seed}"
        
    response = requests.get(url, timeout=45)
    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content))
    else:
        raise Exception(f"Pollinations API failed with status code {response.status_code}: {response.text}")

def generate_image_huggingface(prompt, size="1024x1024", api_key=None):
    """
    Generates an image using Hugging Face Inference API (Requires free HF Token).
    Uses black-forest-labs/FLUX.1-schnell or stabilityai/stable-diffusion-xl-base-1.0.
    """
    if not api_key:
        api_key = get_api_key("huggingface")
        
    if not api_key:
        raise ValueError("Hugging Face API key is missing. Add HUGGINGFACE_API_KEY to your .env file or Streamlit secrets.")
        
    # We will use black-forest-labs/FLUX.1-schnell as it is extremely fast and high quality
    api_url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # FLUX.1-schnell accepts inputs as standard text
    payload = {
        "inputs": prompt,
        "parameters": {
            "num_inference_steps": 4, # FLUX.1-schnell runs in 4 steps
        }
    }
    
    response = requests.post(api_url, headers=headers, json=payload, timeout=60)
    
    # Hugging face models might be loading, return 503. Handle it gracefully
    if response.status_code == 503:
        raise Exception("Hugging Face model is loading. Please try again in a few seconds.")
    elif response.status_code != 200:
        raise Exception(f"Hugging Face API failed with status {response.status_code}: {response.text}")
        
    return Image.open(io.BytesIO(response.content))

def generate_image_openai(prompt, size="1024x1024", api_key=None, model="dall-e-3"):
    """
    Generates an image using OpenAI DALL-E (Requires paid OpenAI API key).
    """
    if not api_key:
        api_key = get_api_key("openai")
        
    if not api_key:
        raise ValueError("OpenAI API key is missing. Add OPENAI_API_KEY to your .env file or Streamlit secrets.")
        
    api_url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size,
        "response_format": "b64_json"
    }
    
    response = requests.post(api_url, headers=headers, json=payload, timeout=60)
    
    if response.status_code != 200:
        raise Exception(f"OpenAI API failed with status {response.status_code}: {response.text}")
        
    response_data = response.json()
    import base64
    b64_data = response_data['data'][0]['b64_json']
    image_data = base64.b64decode(b64_data)
    return Image.open(io.BytesIO(image_data))

def generate_image(prompt, style_name, provider="pollinations", size="1024x1024", negative_prompt=None, seed=None):
    """
    Main entrypoint for generating images. Routes requests to the selected provider.
    """
    # Import and enhance prompt in src.prompts
    from src.prompts import enhance_prompt, get_style_info
    
    final_prompt = enhance_prompt(prompt, style_name)
    style_info = get_style_info(style_name)
    
    # Combine style-conditioned negative prompt with user-supplied negative prompt
    style_negative = style_info.get("negative", "")
    if negative_prompt:
        combined_negative = f"{style_negative}, {negative_prompt}" if style_negative else negative_prompt
    else:
        combined_negative = style_negative
        
    if provider == "pollinations":
        return generate_image_pollinations(
            prompt=final_prompt,
            size=size,
            negative_prompt=combined_negative,
            seed=seed
        ), final_prompt
    elif provider == "huggingface":
        return generate_image_huggingface(
            prompt=final_prompt,
            size=size
        ), final_prompt
    elif provider == "openai":
        # DALL-E 3 doesn't support custom negative prompts directly via parameter,
        # but the prompt styling itself contains negative directions where needed.
        return generate_image_openai(
            prompt=final_prompt,
            size=size,
            model="dall-e-3"
        ), final_prompt
    else:
        raise ValueError(f"Unknown provider: {provider}")
