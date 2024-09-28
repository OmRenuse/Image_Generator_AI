import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import os
import re
import uuid

def generate_image(prompt):
    # Load Stable Diffusion model and tokenizer, defaulting to GPU if available
    model_id = "CompVis/stable-diffusion-v1-4"
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    if torch.cuda.is_available():
        pipe.to("cuda")
    
    # Generate an image from the prompt
    image = pipe(prompt).images[0]

    # Ensure the directory exists
    output_dir = 'static/images'
    os.makedirs(output_dir, exist_ok=True)

    # Clean prompt to use in filenames
    safe_prompt = re.sub(r'[\\/*?:"<>|]', "", prompt)  # Remove invalid characters for file names

    # Use a UUID for the image name to avoid collisions
    image_filename = f"{safe_prompt[:50]}_{uuid.uuid4().hex}.png"  # Truncate prompt to 50 chars for filename
    image_path = os.path.join(output_dir, image_filename)

    # Return both the image object and the path (for later use if needed)
    return image, image_path
