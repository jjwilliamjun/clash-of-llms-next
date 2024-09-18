import math
import os
import datetime
from flask import Flask, send_file, jsonify, request
from flask_cors import CORS, cross_origin
import json
import random
from excel_export import *
from import_excel import *
from class_api import team
from set_parameters import *
import game_data
from create_node_network.create_network import * 
 
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Directory to store uploaded LLM files under excel_api/llm_files
LLM_DIRECTORY = os.path.join(os.path.dirname(__file__), 'llm_files')
os.makedirs(LLM_DIRECTORY, exist_ok=True)

# Global variables to store game data and team settings
game_data = GameData()  
turn_counter=0
red_team = None
blue_team = None
green_team = None
winning_pop_percent = 80
custom_llms = {}  # Placeholder to store custom LLMs

def save_llm_file(team_key, file):
    """Saves the uploaded LLM file for the specified team in the llm_files directory"""
    try:
        # Construct the path to save the file in the llm_files directory
        file_path = os.path.join(LLM_DIRECTORY, f"{team_key}_{file.filename}")
        file.save(file_path)
    except Exception as e:
        print(f"Error saving LLM file: {e}")


@app.route('/excel_api/upload_llm', methods=['POST'])
@cross_origin()
def upload_llm():
    """Handles the upload of an LLM JSON file and saves it to the llm_files directory"""
    try:
        # Check if a file is part of the request
        if 'llm_file' not in request.files:
            return jsonify({"error": "No LLM file provided"}), 400

        file = request.files['llm_file']
        # Ensure the file is a JSON file
        if not file.filename.endswith('.json'):
            return jsonify({"error": "Invalid file type. Only JSON files are allowed."}), 400

        # Save the file using the save_llm_file function
        save_llm_file('custom', file)  # 'custom' is used as a prefix for the uploaded file

        return jsonify({"message": f"LLM file '{file.filename}' uploaded successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/excel_api/excel_import', methods=['POST'])
@cross_origin()
def import_excel():
    """Handles the import of Excel files or random generation of network data"""
    node_attributes = None
    node_connections = None
    global green_team
    try:
        if request.files:
            for key, file_storage in request.files.items():
                file = request.files[key]
                file_path = os.path.join('/tmp', file.filename)
                file.save(file_path)
                
                if key == 'settings_file':
                    teams = import_settings(file_path)

                    if len(teams) > 0:
                        if teams[0] == "errors":
                            errors = teams[1:]
                            return jsonify({"error": errors}), 400

                    global red_team
                    red_team = set_team(teams[0])
                    
                    global blue_team
                    blue_team = set_team(teams[1])

                elif key == 'attributes_file':
                    nodes = import_node_attributes(file_path)
                    node_attributes = nodes  # Save for network creation
                    
                elif key == 'connections_file':
                    connections = import_node_connections(file_path)
                    node_connections = connections  # Save for network creation

                elif key in ['red_team_llm', 'blue_team_llm']:
                    # Save the uploaded LLM file for the red or blue team
                    save_llm_file(key, file)  # Use the save_llm_file function here

            # Ensure both node_attributes and node_connections are available
            if node_attributes and node_connections:
                # Create the network and save it as a JSON file
                network_graph=create_node_network(node_attributes, node_connections)
                blue_alignment, red_alignment=convert_alignment_to_node_count(network_graph, red_team._alignment, blue_team._alignment)
                green_team=GreenTeam(network_graph, blue_alignment,red_alignment)
                return jsonify({"message": "Network created successfully from Excel files!"}), 200
            else:
                return jsonify({"error": "Missing node attributes or connections"}), 400

        elif request.json:
            if request.json.get('defaultOption') == 'random':
                # Handle random generation
                node_count = request.json.get('nodeCount', random.randint(30, 50))  # Generate a random node count between 30 and 50
                node_attributes, node_connections = generate_random_network(node_count)
            
            elif request.json.get('defaultOption') == 'userInput':
                # Handle user input network generation
                node_count = request.json.get('nodeCount', random.randint(30, 50))  # Use the user-provided node count or default to 30-50
                connections_per_node = request.json.get('connectionsPerNode', 3)  # Use the user-provided connections per node or default to 3
                node_attributes, node_connections = generate_user_input_network(node_count, connections_per_node)
            
            else:
                return jsonify({"error": "Invalid option provided"}), 400

            # Create the network and save it as a JSON file
            network_graph=create_node_network(node_attributes, node_connections)
            blue_alignment, red_alignment=convert_alignment_to_node_count(network_graph, red_team._alignment, blue_team._alignment)
            green_team=GreenTeam(network_graph, blue_alignment,red_alignment) #change alignment initial values
            return jsonify({"message": "Network generated successfully!"}), 200
        
        else:
            return jsonify({"error": "No files or valid JSON provided"}), 400

    except Exception as e:
        print(f"Error during file upload: {e}")
        return jsonify({"error": str(e)}), 500

def convert_alignment_to_node_count(graph, red, blue):
    size= graph.number_of_nodes()
    blue_alignment= math.floor((blue / 100) * size)
    red_alignment=math.floor((red / 100) * size)
    if blue_alignment + red_alignment > size:
        print('ERROR')
        return jsonify({"error": "Alignment percentages must sum up to 100. Please enter valid percentages."}), 400
    print('as node count with size',graph.number_of_nodes(),blue_alignment, red_alignment)
    return blue_alignment, red_alignment

# Route to serve the JSON file for a specific round
@app.route('/excel_api/round_data/<int:round_number>', methods=['GET'])
@cross_origin()
def serve_round_data(round_number):
    """Serves the JSON file for the specified round"""
    # Construct the filename and path based on the round number
    json_filename = f'round_{round_number}.json'
    json_path = os.path.join(os.getcwd(), 'excel_api', 'create_node_network', 'round_data', json_filename)
    
    # Check if the file exists and serve it
    if os.path.exists(json_path):
        return send_file(json_path, as_attachment=False, mimetype='application/json')
    else:
        return jsonify({"error": f"Round JSON file not found: {json_filename}"}), 404

# Route to serve LLM file for a specific team
@app.route('/llm_file/<team_colour>', methods=['GET'])
def serve_llm_file(team_colour):
    """Serves the uploaded LLM file for the specified team"""
    if team_colour not in ['red', 'blue']:
        return jsonify({"error": "Invalid team colour"}), 400
    
    file_name = f"{team_colour}_team_llm"
    file_path = os.path.join(LLM_DIRECTORY, file_name)

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=False, mimetype='application/octet-stream')
    else:
        return jsonify({"error": "LLM file not found"}), 404
# Route to fetch Model_IDs from JSON files in the llm_files directory
@app.route('/excel_api/get_llm_models', methods=['GET'])
def get_llm_models():
    """Fetches the list of Model_IDs from the JSON files in the llm_files directory"""
    model_ids = []

    try:
        for filename in os.listdir(LLM_DIRECTORY):
            if filename.endswith('.json'):
                file_path = os.path.join(LLM_DIRECTORY, filename)
                with open(file_path, 'r') as file:
                    llm_data = json.load(file)
                    if 'Model_ID' in llm_data:
                        model_ids.append(llm_data['Model_ID'])

        return jsonify(model_ids), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to fetch team parameters
@app.route('/excel_api/get_parameters', methods=['GET'])
@cross_origin()
def get_parameters():
    """Fetches the parameters for the Red and Blue teams"""
    global blue_team
    global red_team

    if blue_team is None or red_team is None: 
        return jsonify({"error": "Parameters not found"}), 404

    output = [red_team.__dict__, blue_team.__dict__]
    
    return jsonify(output), 200

# Route to handle UI parameters input
@app.route('/excel_api/ui_parameters', methods=['POST'])
@cross_origin()
def ui_parameters():
    """Handles the UI parameters input, including random network generation"""
    global green_team
    try:
        parameters = request.get_json()

        global red_team
        red_team = set_team(parameters['red_team'])

        global blue_team
        blue_team = set_team(parameters['blue_team'])

        if parameters.get('green_node_count_option') == 'random':
            node_count = random.randint(30, 50)  # Adjust the range as needed
            node_attributes, node_connections = generate_random_network(node_count)
        
        elif parameters.get('green_node_count_option') == 'userInput':
            node_count = parameters.get('green_nodes_count')
            connections_per_node = parameters.get('connections_per_node', 3)  # Default to 3 connections per node
            node_attributes, node_connections = generate_user_input_network(node_count, connections_per_node)
        
        else:
            return jsonify({"error": "Invalid green_node_count_option"}), 400

        network_graph=create_node_network(node_attributes, node_connections)
        blue_alignment, red_alignment=convert_alignment_to_node_count(network_graph, red_team._alignment, blue_team._alignment)
        green_team=GreenTeam(network_graph, blue_alignment,red_alignment)

        return jsonify({"message": "Network generated successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return '', 200


@app.route('/excel_api/excel_export', methods=['GET'])
def export_excel():
    """Exports game data to Excel"""
    try:
        if game_data is None:
            return jsonify({"error": "No game data available"}), 400
        excel_file = export_data_excel(game_data)

        if excel_file is None:
            return jsonify({"error": "Failed to generate the Excel file"}), 500
        #now = datetime.now()
        #timestamp = now.strftime("%H_%M_%S")
        excel_file_name = f"clash_of_llms.xlsx"
        return send_file(
            excel_file,
            download_name=excel_file_name,
            as_attachment=True,   
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
# Route to serve next round request from the frontend
@app.route('/excel_api/next_round', methods=['GET'])
@cross_origin()
def start_next_round():
    global turn_counter
    global green_team
    turn_data=GameTurnData()
    turn_counter = turn_counter + 1
    msg_content = []
    victor = None

    team_colour = request.args.get('team')
    
    if blue_team is None or red_team is None: 
        return jsonify({"error": "Team not found"}), 404
    
    # Assignment of current team
    if team_colour == 'red':
        current_team = red_team
    elif team_colour == 'blue':
        current_team = blue_team
    else:
        return jsonify({"error": "Incorrect team colour"}), 404
    
    # Update alignment for the two teams
    red_team._alignment = green_team.red_alignment()
    blue_team._alignment = green_team.blue_alignment()

    # Generate message and update green network
    current_team.generate_message()
    if (not isinstance(current_team._potency, str)):
        green_team.broadcast_message(current_team._potency, current_team._team, current_team._influence_factor)
        green_team.update_green_network()

        # Add the new function to create and save a JSON file for the current round
        create_round_json(turn_counter, green_team._network_graph)
    
    # Update energy level if the current team is blue
    if current_team._team.lower() == 'blue':
        energy_cost = current_team.energy_cost()
        current_team.update_energy_level(energy_cost)
    
    print(f'Current team has alignment {current_team._alignment}%')
    
    # Winning by majority support
    if red_team._alignment >= winning_pop_percent:
        victor = red_team._team
    elif blue_team._alignment >= winning_pop_percent:
        victor = blue_team._team
    
    # Winning by energy loss
    if current_team._team.lower() == 'blue' and current_team._energy == 0:
        victor = 'Red'
    
    #Reset turn counter if winner is determined
    #TODO: move this to start of loop potentially

    
    msg_content.append(current_team._message)
    msg_content.append(current_team._potency)
    msg_content.append(victor)
    msg_content.append(red_team.__dict__)
    msg_content.append(blue_team.__dict__)
    turn_data.set_all_turn_data(turn_counter, current_team._team, current_team._message, current_team._potency, current_team._energy, green_team.red_alignment(), green_team.blue_alignment())
    game_data.add_entry(turn_data)
    if victor:
        turn_counter = 0
    print(f'Blue team has {blue_team._energy} energy left')
    return jsonify(msg_content), 200

def create_round_json(round_number, network_graph):
    """Creates a JSON file for the network graph for the given round"""
    # Convert the graph to node-link data format
    graph_data = nx.node_link_data(network_graph)
    
    # Define the path to save the JSON file (e.g., round_1.json, round_2.json)
    json_filename = f'round_{round_number}.json'
    json_path = os.path.join(os.getcwd(), 'excel_api', 'create_node_network', 'round_data', json_filename)

    # Ensure the 'round_data' directory exists
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    # Save the graph data to the JSON file
    try:
        with open(json_path, 'w') as f:
            json.dump(graph_data, f, indent=4)
        print(f"Round {round_number} JSON file successfully created at: {json_path}")
    except Exception as e:
        print(f"Failed to save Round {round_number} JSON file: {str(e)}")


if __name__ == '__main__':
    #game_data = generate_game_data()  # Testing purposes
    app.run(debug=True)
