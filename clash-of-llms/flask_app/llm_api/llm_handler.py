import importlib.util
import os

def load_custom_handler(team: str):
    """Dynamically loads the handler for the custom model."""
    handler_path = os.path.join('models', team, 'handler.py')

    # Dynamically load the handler.py script
    spec = importlib.util.spec_from_file_location("handler", handler_path)
    handler = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(handler)

    return handler

def run_custom_model(team: str, input_data):
    """Runs the custom model for the specified team."""
    try:
        handler = load_custom_handler(team)
        potency = handler.predict(input_data)  # Assuming the handler has a predict() method
        return potency
    except Exception as e:
        print(f"Error running custom model: {e}")
        return None

def calculate_message_potency(team, model_ID, alignment, temperature, msg_count, energy):
    if model_ID == 'custom':
        input_data = {
            'alignment': alignment,
            'temperature': temperature,
            'msg_count': msg_count,
            'energy': energy
        }
        return run_custom_model(team, input_data)
    else:
        # Existing logic for GPT or other LLM
        return get_message(team, model_ID, alignment, temperature, msg_count, energy)
