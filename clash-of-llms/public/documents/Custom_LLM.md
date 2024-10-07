
# Custom LLM Integration Guide

This guide explains how to upload, integrate, and modify custom LLMs (including PyTorch, TensorFlow, or other custom formats) in the system.

## 1. Upload Custom LLM Files

Researchers can upload their own custom LLM models, regardless of the framework.

-   **Supported File Formats:** `.pt` for PyTorch, `.h5` for TensorFlow, or **any custom file format**.
-   **Storage Directory:** Files are saved in `flask_app/llm_api/llm_files`.
-   **Automatic File Naming:** The system will automatically add the corresponding team prefix (`blue_` or `red_`) to the uploaded file name when saving.

If uploading files manually, place them in `flask_app/llm_api/llm_files`.

### Metadata Requirements

All custom models must include metadata to ensure proper integration:

**Example Metadata Structure:**

```python
metadata = {
    "model_ID": "simple_model",
    "team": "blue",
    "description": "This is a custom model for testing purposes.",
    "version": "1.0",
    "author": "Test User",
    "date_created": "2024-10-04",
    "use_case": "Basic model for testing functionality."
}
``` 

**Saving Metadata Example (PyTorch):**

```python
torch.save({
    'model_state_dict': model.state_dict(),
    'metadata': metadata
}, 'simple_model.pt')
``` 

**Key Metadata Fields:**

-   `model_ID`: Unique identifier for the model.
-   `team`: The team this model is used for ("blue" or "red").
-   Additional fields like `description`, `author`, etc., help in tracking the model information.

## 2. Modify `llm_handler.py` for LLM Integration

`llm_handler.py` is responsible for loading and running custom models. You can modify it to integrate either a PyTorch, TensorFlow, or any other custom model format.

### PyTorch Model Integration

To integrate a PyTorch model, use the following function:

```python
def serve_pytorch_model(model_file, input_data):
    checkpoint = torch.load(model_file, map_location='cpu')  # Load the PyTorch model
    model = SimpleModel()  # Initialize your model architecture
    model.load_state_dict(checkpoint['model_state_dict'])  # Load the saved state
    model.eval()  # Set the model to evaluation mode
    
    # Extract metadata if present
    metadata = checkpoint.get('metadata', {})

    input_tensor = torch.tensor(input_data)  # Convert input data to a PyTorch tensor
    with torch.no_grad():  # Run inference without gradients
        output = model(input_tensor)  # Run the model
    return output, metadata  # Return the output along with metadata 
```
### TensorFlow Model Integration

For TensorFlow models:

```python
def serve_tensorflow_model(model_file, input_data):
    model = tf.keras.models.load_model(model_file)  # Load the TensorFlow model
    input_tensor = tf.convert_to_tensor(input_data)  # Convert input data into a TensorFlow tensor
    output = model(input_tensor)  # Run inference
    return output  # Return the output
```

### Custom Model Integration

If researchers have their own model format, they must add a custom serving function:

```python
def serve_custom_model(model_file, input_data):
    # Implement your logic for loading and running inference with your custom model
    # Example: Deserialize the model, run on input_data, and return the output
    pass
```

## 3. Update the `serve_llm` Function

To incorporate different LLM types, update the `serve_llm` function in `llm_handler.py`:

```python
def serve_llm(team, input_data):
    try:
        model_file = load_model(team)  # Load the model file for the team

        # Identify the model type and serve accordingly
        if model_file.endswith('.pt'):
            return serve_pytorch_model(model_file, input_data)
        elif model_file.endswith('.h5'):
            return serve_tensorflow_model(model_file, input_data)
        else:
            return serve_custom_model(model_file, input_data)

    except Exception as e:
        print(f"Error serving model for {team}: {e}")
        return None
```
## 4. Uploading and Using Custom Models

### Step 1: Upload the Custom Model

-   Use the frontend interface to select "Custom" during team setup and upload the model file.
-   The system will automatically detect the team and save the model with the correct team prefix.

### Step 2: Backend Processing

-   The model type is identified based on the file extension, or handled generically for custom formats.
-   The appropriate serving function is used for inference during the simulation.

## 5. Example Workflow for Custom LLM

-   **Upload the Model File:** During team setup, select "Custom" and upload the PyTorch, TensorFlow, or any other custom model file.
-   **Inference During Simulation:** During each simulation round, the uploaded model is used to generate messages or perform other actions.
-   **Metadata Handling:** Metadata is used to display model details during the simulation.

### Example Input and Output Handling

-   **Input Data:** The input data for custom models is passed as a Python dictionary that includes values such as:
    -   `alignment`
    -   `temperature`
    -   `msg_count`
    -   `energy`

```python
input_data = {
    'alignment': 50,
    'temperature': 0.7,
    'msg_count': 3,
    'energy': 100
}
```

-   **Output Example:**

```python
message = "This is a generated message."
potency = 85.6
```

The system takes the output and uses it during the simulation to influence team strategies and node behaviors.

## 6. Displaying Metadata in the Frontend

-   **Metadata Utilization:** The metadata in the model files is crucial for displaying information about the model during each round of the simulation.
-   **Frontend Integration:** Metadata fields (e.g., `model_ID`, `description`) are used to update the display for the team models:

```javascript
{{ blue_metadata ? blue_metadata.model_ID : blue_team._model_ID }}
```

This ensures consistent display of model identifiers and metadata during each round of the simulation.

## 7. Summary

-   **Upload Custom Models:** Upload your PyTorch, TensorFlow, or other custom models during team setup.
-   **Include Metadata:** All models must include metadata to ensure proper display and identification.
-   **Simulation Ready:** Models are automatically loaded, and the system will utilize the output to drive simulation rounds.