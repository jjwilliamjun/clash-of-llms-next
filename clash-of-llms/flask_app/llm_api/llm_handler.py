import os
import importlib.util
import torch  # For PyTorch (placeholder)
import tensorflow as tf  # For TensorFlow (placeholder)
from llm_api.llm_handler import *
from class_api.gpt_endpoint import *

def load_model(team):
    """Load a custom LLM model for the specified team."""
    model_file = None
    model_dir = os.path.join('flask_app', 'llm_api', 'llm_files')

    # Look for the team-specific model in the directory
    for filename in os.listdir(model_dir):
        if filename.startswith(f"{team.lower()}_"):
            model_file = os.path.join(model_dir, filename)
            break

    if not model_file:
        raise FileNotFoundError(f"No model found for {team} team")

    return model_file


def serve_llm(team, input_data):
    """Serve the LLM model for the specified team."""
    try:
        model_file = load_model(team)

        # Check if it's a PyTorch or TensorFlow model based on file extension
        if model_file.endswith('.pt') or model_file.endswith('.pth'):
            # This is a PyTorch model (for future use)
            return serve_pytorch_model(model_file, input_data)
        elif model_file.endswith('.h5') or model_file.endswith('.pb'):
            # This is a TensorFlow model (for future use)
            return serve_tensorflow_model(model_file, input_data)
        else:
            raise ValueError("Unknown model format. Expected PyTorch (.pt/.pth) or TensorFlow (.h5/.pb)")

    except FileNotFoundError as fnf_error:
        # Log and use GPT-3.5 as fallback
        print(f"{fnf_error} - Falling back to GPT-3.5")
        return run_custom_model(team, input_data)

    except Exception as e:
        print(f"Error serving model for {team} team: {e}")
        return None


def serve_pytorch_model(model_file, input_data):
    """Placeholder for serving a PyTorch model."""
    # Check if torch is installed, else return placeholder
    try:
        print(f"Serving PyTorch model from {model_file} with input data: {input_data}")

        # Load the PyTorch model
        model = torch.load(model_file)
        model.eval()  # Set the model to evaluation mode
        
        # Convert input_data to a tensor (future logic will determine the structure of input_data)
        input_tensor = torch.tensor(input_data)
        
        # Run inference (this will be tailored based on the actual model structure)
        with torch.no_grad():
            output = model(input_tensor)
        
        return output
    except ImportError:
        print("PyTorch is not installed. Please install it to use PyTorch models.")
        return None


def serve_tensorflow_model(model_file, input_data):
    """Placeholder for serving a TensorFlow model."""
    try:
        print(f"Serving TensorFlow model from {model_file} with input data: {input_data}")
        
        # Load the TensorFlow model
        model = tf.keras.models.load_model(model_file)
        
        # Convert input_data to a format TensorFlow can handle (future logic will adapt this)
        input_tensor = tf.convert_to_tensor(input_data)
        
        # Run inference
        output = model(input_tensor)
        
        return output
    except ImportError:
        print("TensorFlow is not installed. Please install it to use TensorFlow models.")
        return None


def run_custom_model(team, input_data):
    """Placeholder function for custom model integration."""
    # Placeholder for future custom model execution
    # Right now, we use GPT-3.5 to generate messages

    # Log that we're using a placeholder
    print(f"Using GPT-3.5 as placeholder for {team} team.")

    # Set up default GPT-3.5 model usage for now
    model_id = "gpt-3.5-turbo"
    alignment = input_data.get('alignment')
    temperature = input_data.get('temperature')
    msg_count = input_data.get('msg_count')
    energy = input_data.get('energy')

    # Call the existing get_message function
    message, potency = get_message(team, model_id, alignment, temperature, msg_count, energy)

    return message, potency

