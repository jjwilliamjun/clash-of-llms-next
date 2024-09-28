import os
import importlib.util
import torch  # For PyTorch (placeholder)
import tensorflow as tf  # For TensorFlow (placeholder)
from llm_api.llm_handler import *
from class_api.gpt_endpoint import *

LLM_FILES_DIRECTORY = os.path.join('flask_app', 'llm_api', 'llm_files')
os.makedirs(LLM_FILES_DIRECTORY, exist_ok=True)

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
            # Call user-defined model
            result = serve_user_llm(team, input_data)
            if result is None:
                raise ValueError("Unknown model format or user-defined LLM function is not implemented.")
            return result

    except FileNotFoundError as fnf_error:
        # Log and use GPT-3.5 as fallback
        print(f"{fnf_error} - Falling back to GPT-3.5")
        return run_custom_model(team, input_data)

    except Exception as e:
        print(f"Error serving model for {team} team: {e}")
        return None


def serve_pytorch_model(model_file, input_data):
    """Placeholder for serving a PyTorch model."""
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
    # Log that we're using GPT-3.5 as a placeholder
    print(f"Using GPT-3.5 as placeholder for {team} team, while model is still 'custom'.")

    # Set up GPT-3.5 model usage for now, while keeping the 'custom' model_id
    model_id = "gpt-3.5-turbo"
    message, potency = get_message(team, model_id, input_data['alignment'], input_data['temperature'], input_data['msg_count'], input_data['energy'])

    return message, potency


def serve_user_llm(team, input_data):
    """Placeholder for serving a user-defined LLM model."""
    # This function is intended for the user to modify to integrate their custom LLM
    # By default, this function returns None to indicate it has not been implemented yet.
    print(f"Attempting to serve a user-defined LLM for team: {team}")
    return None
