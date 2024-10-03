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
    model_dir = LLM_FILES_DIRECTORY

    try:
        # Look for the team-specific model in the directory
        for filename in os.listdir(model_dir):
            if filename.startswith(f"{team.lower()}_"):
                model_file = os.path.join(model_dir, filename)
                break

        if not model_file:
            raise FileNotFoundError(f"No model found for {team} team")

        # Load model and extract metadata
        model_metadata = get_metadata(model_file)

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        raise
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

    return model_file, model_metadata

def extract_metadata(model_file):
    """Extract metadata from the LLM file."""
    metadata = {}
    try:
        if model_file.endswith(('.pt', '.pth')):
            # PyTorch model case with weights_only=True for security
            checkpoint = torch.load(model_file, map_location='cpu', weights_only=True)
            metadata = checkpoint.get('metadata', {})
        elif model_file.endswith(('.h5', '.pb')):
            # TensorFlow model case (assuming metadata is saved in a specific way)
            model = tf.keras.models.load_model(model_file)
            metadata = getattr(model, 'metadata', {})
        else:
            # Handle other user-defined models or formats (like Python files)
            print(f"Unknown format for extracting metadata: {model_file}")

    except Exception as e:
        print(f"Error extracting metadata from {model_file}: {e}")

    return metadata



def get_metadata(model_file):
    """Extract metadata from the model file."""
    metadata = {}
    try:
        if model_file.endswith(('.pt', '.pth')):
            # PyTorch model case
            checkpoint = torch.load(model_file, map_location='cpu')
            metadata = checkpoint.get('metadata', {})
            if not metadata:
                print(f"No metadata found in {model_file}, using default metadata.")
        elif model_file.endswith(('.h5', '.pb')):
            # TensorFlow model case (assuming metadata is saved in a specific way)
            model = tf.keras.models.load_model(model_file)
            metadata = getattr(model, 'metadata', {})
            if not metadata:
                print(f"No metadata found in {model_file}, using default metadata.")
    except Exception as e:
        print(f"Error extracting metadata from {model_file}: {e}")
    
    return metadata




def serve_llm(team, input_data):
    """Serve the LLM model for the specified team."""
    try:
        model_file, model_metadata = load_model(team)

        # Check if it's a PyTorch or TensorFlow model based on file extension
        if model_file.endswith('.pt') or model_file.endswith('.pth'):
            return serve_pytorch_model(model_file, input_data, model_metadata)
        elif model_file.endswith('.h5') or model_file.endswith('.pb'):
            return serve_tensorflow_model(model_file, input_data, model_metadata)
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



def serve_pytorch_model(model_file, input_data, metadata):
    """Serve a PyTorch model with metadata."""
    try:
        print(f"Serving PyTorch model from {model_file} with input data: {input_data}")

        # Load the PyTorch model
        checkpoint = torch.load(model_file, map_location='cpu')
        model = checkpoint.get('model')
        model.eval()  # Set the model to evaluation mode

        # Convert input_data to a tensor (future logic will determine the structure of input_data)
        input_tensor = torch.tensor(input_data)

        # Run inference (this will be tailored based on the actual model structure)
        with torch.no_grad():
            output = model(input_tensor)

        return {"output": output.tolist(), "metadata": metadata}
    except ImportError:
        print("PyTorch is not installed. Please install it to use PyTorch models.")
        return None

def serve_tensorflow_model(model_file, input_data, metadata):
    """Serve a TensorFlow model with metadata."""
    try:
        print(f"Serving TensorFlow model from {model_file} with input data: {input_data}")

        # Load the TensorFlow model
        model = tf.keras.models.load_model(model_file)

        # Convert input_data to a format TensorFlow can handle (future logic will adapt this)
        input_tensor = tf.convert_to_tensor(input_data)

        # Run inference
        output = model(input_tensor)

        return {"output": output.numpy().tolist(), "metadata": metadata}
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
    # Log that we're attempting to use a user-defined LLM
    print(f"Attempting to serve a user-defined LLM for team: {team}")

    # This function can be extended to include user-defined models
    # Metadata should also be managed appropriately here.
    metadata = {"info": f"Metadata not available for custom LLM for {team} team."}
    return {"output": "User-defined LLM output", "metadata": metadata}

