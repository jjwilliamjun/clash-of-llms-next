
# Custom LLM Integration Guide

This guide explains how to upload, integrate, and modify custom LLMs (PyTorch or TensorFlow) in the system.

## 1. Upload Custom LLM Files

Custom LLMs can be uploaded via the frontend during the team setup (Blue or Red team).

-   **Supported File Formats:** `.pt` for PyTorch or `.h5` for TensorFlow models.
-   **Storage Directory:** The files will be saved in the `flask_app/llm_api/llm_files` directory.
-   **Naming Convention:**
    -   `blue_custom_model.pt` or `blue_custom_model.h5`
    -   `red_custom_model.pt` or `red_custom_model.h5`

If uploading files manually, place them directly in the `flask_app/llm_api/llm_files` directory.


## 2. Modify `llm_handler.py` for LLM Integration

`llm_handler.py` is responsible for loading and running custom models. You’ll need to modify the appropriate handler to integrate either a PyTorch or TensorFlow model based on the type of LLM being used. Here’s how to do that:

### PyTorch Model Integration

To integrate a PyTorch model, follow these steps:

1.  **Locate the `serve_pytorch_model` function in `llm_handler.py`.**
2.  **Modify the function to load and run inference on PyTorch models using the code snippet below:**

```python
def serve_pytorch_model(model_file, input_data):
    model = torch.load(model_file)  # Load the PyTorch model from the given file
    model.eval()  # Set the model to evaluation mode, important for inference
    input_tensor = torch.tensor(input_data)  # Convert input data to a PyTorch tensor
    with torch.no_grad():  # Ensure that gradients are not calculated to save memory
        output = model(input_tensor)  # Run the model to get predictions
    return output  # Return the output of the model
```
-   **Key Adjustments**:
    -   Ensure the input data format matches the model's expected input (for example, if your model expects a specific shape for the input tensor, reshape it as needed).
    -   Ensure the output format matches the type of results you expect (e.g., messages and potency).

### TensorFlow Model Integration

To integrate a TensorFlow model, follow these steps:

1.  **Locate the `serve_tensorflow_model` function in `llm_handler.py`.**
2.  **Modify the function to load and run inference on TensorFlow models using the code snippet below:**

```python
def serve_tensorflow_model(model_file, input_data):
    model = tf.keras.models.load_model(model_file)  # Load the TensorFlow model
    input_tensor = tf.convert_to_tensor(input_data)  # Convert input data into a TensorFlow tensor
    output = model(input_tensor)  # Run the model on the input data
    return output  # Return the output of the model
```

-   **Key Adjustments**:
    -   Ensure the input data is in a format that the model can process.
    -   TensorFlow models often expect inputs with a specific shape, so adjust the input format accordingly.
    -   The `output` should be parsed and returned as the required format (e.g., generated message and potency).


## 3. Add New LLM Types (Optional)

To integrate other model types (e.g., Hugging Face models), follow these steps:

1.  **Create a New Function:**  
    You’ll need to create a new function that loads and runs the desired model format (e.g., for Hugging Face models). The function should handle loading the model, processing the input, and returning the appropriate output.
    
2.  **Modify the `serve_llm` Function:**  
    Modify the `serve_llm` function to detect and recognize the new model format (for instance, based on the model file extension or type). Then, route it to the correct handler function for inference.
    

### Example: Hugging Face Model Integration

Hugging Face models can be integrated using the `transformers` library. Here's how you can update `llm_handler.py` to include Hugging Face model support:

1.  **Install the Hugging Face Transformers Library:** To use Hugging Face models, you need to install the `transformers` library:
    
```bash
pip install transformers 
```
2.  **Create the `serve_transformers_model` Function:**
    
    This function will use the Hugging Face `pipeline` API for inference. You can load a pre-trained model and run it on the input data (which could be a text prompt).
    
```python
   from transformers import pipeline
    
    def serve_transformers_model(model_file, input_data):
        # Create a Hugging Face pipeline for text generation or other tasks
        model = pipeline('text-generation', model=model_file)
    
        # Ensure that the input data contains text for the Hugging Face model
        if 'text' not in input_data:
            raise ValueError("Input data must contain 'text' key for Hugging Face model")
    
        # Run the Hugging Face model on the input text
        output = model(input_data['text'])
        return output` 
```
    -   **Task Type:** You can specify different task types for the Hugging Face pipeline (e.g., `'text-generation'`, `'text-classification'`, `'sentiment-analysis'`, etc.). Modify this according to the model's purpose.
    -   **Input Format:** Ensure the input data contains the necessary fields (`'text'` in this example).
3.  **Modify the `serve_llm` Function:**
    
    After adding the new model handler, you need to update the `serve_llm` function to detect when a Hugging Face model is in use. You can base this on the model file extension or another identifying factor.
    
```python
   def serve_llm(team, input_data):
        try:
            model_file = load_model(team)  # Load the correct model file for the team
    
            # Check if it's a PyTorch model
            if model_file.endswith('.pt') or model_file.endswith('.pth'):
                return serve_pytorch_model(model_file, input_data)
    
            # Check if it's a TensorFlow model
            elif model_file.endswith('.h5'):
                return serve_tensorflow_model(model_file, input_data)
    
            # Check if it's a Hugging Face model (assuming a specific file extension or identifier)
            elif model_file.endswith('.transformers'):
                return serve_transformers_model(model_file, input_data)
    
            # Handle unknown model types
            else:
                raise ValueError(f"Unsupported model format: {model_file}")
        
        except Exception as e:
            print(f"Error serving model for {team}: {e}")
            return None
```    

### Key Considerations for Hugging Face Models:

-   **Model Task:** Ensure the task type (e.g., `text-generation`, `text-classification`, etc.) is appropriate for your use case.
-   **Input and Output Handling:** Depending on the task type, the input and output formats may vary. For example, `text-generation` will return generated text, while `text-classification` may return labels or probabilities.
-   **Flexibility:** Hugging Face models are highly customizable, so you can switch between models or tasks by adjusting the `pipeline()` parameters.
```
## 4. Future Custom LLM Integration Steps

Researchers can follow these steps to integrate their own LLM models into the system:

1.  **Upload the Model File:**  
    Upload the model file in the appropriate format (`.pt` for PyTorch or `.h5` for TensorFlow) during the team setup.
    
2.  **Modify `llm_handler.py`:**  
    Implement the logic for running your custom model:
    
    -   Add functions for serving your model if needed.
    -   Configure `serve_llm` to recognize your custom model based on the file extension or model type.

## 5. Example Workflow for Custom LLM

### Step 1: Upload the Custom Model

-   Select "custom" from the frontend dropdown.
-   Upload the model file for the team (Blue or Red).

### Step 2: Backend Processing

-   The system will detect the file in `llm_api/llm_files` and call the appropriate model handler.
-   For example, if a `.pt` file is uploaded, the `serve_pytorch_model` function will be called.

## 6. Input and Output Processing

The input data for custom models is passed as a Python dictionary and may include the following keys:

-   `alignment`: The alignment percentage of the team.
-   `temperature`: The temperature for the LLM model.
-   `msg_count`: The number of messages to generate.
-   `energy`: The current energy level of the team.

### Example Input:

```python
`input_data = {
    'alignment': 50,
    'temperature': 0.7,
    'msg_count': 3,
    'energy': 100
}
```

### Example Output:

```python
message = "This is the best message to send."
potency = 85.6
```

## **7. How Custom LLM Integration Works**

1.  **Upload Your Model:**
    
    -   The system allows users (researchers, developers) to upload their own models for use in simulations.
    -   These models can be in **PyTorch (.pt)**, **TensorFlow (.h5)**, or **Hugging Face** formats.
    -   When setting up a team (Blue or Red) in the simulation, the user selects "Custom" and uploads the model file. The model gets saved in the system.
2.  **Automatic Model Handling:**
    
    -   Once the model is uploaded, the system automatically identifies the model type based on the file extension:
        -   `.pt` or `.pth` = PyTorch Model
        -   `.h5` = TensorFlow Model
        -   `.transformers` or other = Hugging Face Model
    -   Based on the file extension, the system will use the appropriate model loading and inference method.
3.  **Model Types Supported:**
    
    -   **PyTorch Models:**
        -   After the PyTorch model is uploaded, the system loads it and runs inference using the uploaded model's configuration and the input data provided by the simulation.
    -   **TensorFlow Models:**
        -   TensorFlow models are loaded using the TensorFlow library and used for inference with the provided input data.
    -   **Hugging Face Models:**
        -   If the model uploaded is from Hugging Face, the system uses the `transformers` library to run tasks like text generation or classification.
        -   Input data for Hugging Face models must contain text, and the system will use this text to generate output messages based on the model's capabilities.
4.  **How It Works During Simulation:**
    
    -   During each simulation round, the system takes input data (like energy, alignment, etc.) and uses the uploaded model to generate a response.
    -   The output from the model (a generated message or other result) is used in the simulation to influence team strategies, broadcast messages, and update node alignments.
5.  **Automatic Processing of Inputs and Outputs:**
    
    -   Input data like team alignment, temperature, and message counts are passed to the model automatically.
    -   The system then receives the model's output (message and potency) and uses it to calculate the impact of the message in the simulation.

----------

### **Example Workflow for Researchers:**

-   **Step 1: Upload Your Model File**  
    During team setup (either Blue or Red team), the researcher selects the "Custom" option and uploads their model file in one of the supported formats: PyTorch (.pt), TensorFlow (.h5), or Hugging Face (.transformers).
    
-   **Step 2: Model Execution**  
    When the simulation starts, the system detects the uploaded model and automatically uses the correct method to load and run the model. The model will generate messages or responses based on the input data, like team alignment or energy.
    
-   **Step 3: View Results**  
    The generated messages and their potency (impact) are used to influence the nodes in the simulation. The results can be viewed in the simulation dashboard.
    

----------

### **Summary for Clients:**

-   **Upload:** Upload your custom PyTorch, TensorFlow, or Hugging Face model.
-   **Automatic Handling:** The system will automatically recognize the model type and run it during simulation.
-   **Simulate:** The system uses the model’s output (message and potency) to drive the simulation, adjusting team strategies and node alignments.
