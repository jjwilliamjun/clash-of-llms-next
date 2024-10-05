import math
import os, subprocess
from flask import Flask, send_file, jsonify, request
from flask_cors import CORS, cross_origin
import json
import random
from excel_api.excel_export import *
from excel_api.game_data import GameData
from excel_api.import_excel import *
from excel_api.set_parameters import *
from create_node_network.create_network import *
from create_node_network.green_team import *
from class_api.team import *
from class_api.simulation import *
from class_api.termination import Termination
from llm_api.llm_handler import *

app = Flask(__name__)

# Allow requests from http://localhost: 8080
CORS(app, resources={r"/*": {"origins":"http://127.0.0.1:5000:8080"}})

# Global variables to store game data and team settings
game_data = GameData()  
turn_counter = 0
red_team = None
blue_team = None
green_team = None
custom_llms = {}  # Placeholder to store custom LLMs
game_style = None
continuous_game = None
terminating_conditions = None

@app.route('/upload_llm', methods=['POST'])
@cross_origin()
def upload_llm():
    try:
        if 'llm_file' not in request.files:
            return jsonify({"error": "No LLM file provided"}), 400

        team = request.form.get('team', None)
        if not team or team.lower() not in ['red', 'blue']:
            return jsonify({"error": "Invalid or missing team (expected 'red' or 'blue')"}), 400

        file = request.files['llm_file']
        filename = file.filename

        new_filename = f"{team.lower()}_{filename}"
        llm_files_directory = os.path.join('flask_app', 'llm_api', 'llm_files')
        os.makedirs(llm_files_directory, exist_ok=True)

        file_path = os.path.join(llm_files_directory, new_filename)
        file.save(file_path)

        # Extract metadata from the uploaded model
        metadata = extract_metadata(file_path)
        if metadata:
            # Optionally save metadata for later use
            metadata_path = os.path.join(llm_files_directory, f"{team.lower()}_metadata.json")
            with open(metadata_path, 'w') as meta_file:
                json.dump(metadata, meta_file)

        return jsonify({"message": f"LLM file '{new_filename}' uploaded successfully at '{file_path}'.", "metadata": metadata}), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500


    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_models_metadata', methods=['GET'])
@cross_origin()
def get_models_metadata():
    """Fetch metadata for all available models"""
    try:
        return jsonify(custom_llms), 200  # Return metadata stored in `custom_llms`
    except Exception as e:
        return jsonify({"error": f"Error retrieving model metadata: {str(e)}"}), 500

@app.route('/get_team_metadata/<team>', methods=['GET'])
@cross_origin()
def get_team_metadata(team):
    """Fetches metadata for the specified team (blue or red)"""
    metadata_file_path = os.path.join(LLM_FILES_DIRECTORY, f"{team.lower()}_metadata.json")

    if not os.path.exists(metadata_file_path):
        return jsonify({"error": f"Metadata file for {team} not found"}), 404

    try:
        with open(metadata_file_path, 'r') as f:
            metadata = json.load(f)
        return jsonify(metadata), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/excel_import', methods=['POST'])
@cross_origin()
def import_excel():
    """Handles the import of Excel files or random generation of network data"""
    node_attributes = None
    node_connections = None
    global green_team
    global red_team
    global blue_team
    try:
        if request.files:
            for key, file_storage in request.files.items():
                file = request.files[key]
                file_path = os.path.join('/tmp', file.filename)
                file.save(file_path)
                
                if key == 'settings_file':
                    try: 
                        teams = import_settings(file_path)

                        if len(teams) > 0:
                            if teams[0] == "errors":
                                errors = teams[1:]
                                return jsonify({"error": errors}), 400

                        red_team = set_team(teams[0])
                        blue_team = set_team(teams[1])

                        global terminating_conditions
                        terminating_conditions = Termination(teams[2]['round_number'], teams[2]['population_alignment'])
                    
                    except Exception as e:
                        error_msg = f"Issue found in Simulation Settings file format: {e}"
                        return jsonify({"error": error_msg}), 500
                    

                elif key == 'attributes_file':
                    try:
                        nodes = import_node_attributes(file_path)
                        node_attributes = nodes  # Save for network creation
                        blue_aligned, red_aligned, neutral, errors = validate_attributes(nodes)

                        if len(errors) > 0:
                            return jsonify({"error": errors}), 400
                        
                        red_team._alignment = (red_aligned/len(nodes)) * 100
                        blue_team._alignment = (blue_aligned/len(nodes)) * 100

                    except Exception as e:
                        error_msg = f"Issue found in Node Attributes file format: {e}"
                        print(error_msg)
                        return jsonify({"error": error_msg}), 500
                    
                elif key == 'connections_file':
                    try:
                        connections = import_node_connections(file_path)
                        errors = validate_connections(connections, nodes)

                        if len(errors) > 0:
                            return jsonify({"error": errors}), 400
                        
                        node_connections = connections  # Save for network creation
                    except Exception as e:
                        error_msg = f"Issue found in Node Connections file format: {e}"
                        print(error_msg)
                        return jsonify({"error": error_msg}), 500

                elif key in ['red_team_llm', 'blue_team_llm']:
                    # Save the uploaded LLM file for the red or blue team
                    save_llm_file(key, file)  # Use the save_llm_file function here

            # Ensure both node_attributes and node_connections are available
            if node_attributes and node_connections:
                # Create the network and save it as a JSON file
                network_graph = create_node_network(node_attributes, node_connections)
                blue_alignment, red_alignment = convert_alignment_to_node_count(network_graph, red_team._alignment, blue_team._alignment)
                green_team = GreenTeam(network_graph, blue_alignment,red_alignment)
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
            print(f"Error (400) during file upload: {e}")
            return jsonify({"error": "No files or valid JSON provided"}), 400

    except Exception as e:
        print(f"Error (500) during file upload: {e}")
        return jsonify({"error": str(e)}), 500

def convert_alignment_to_node_count(graph, red, blue):
    size = graph.number_of_nodes()
    blue_alignment= math.floor((blue / 100) * size)
    red_alignment=math.floor((red / 100) * size)
    if blue_alignment + red_alignment > size:
        return jsonify({"error": "Alignment percentages must sum up to 100. Please enter valid percentages."}), 400
    print('as node count with size',graph.number_of_nodes(),blue_alignment, red_alignment)
    return blue_alignment, red_alignment

# Route to serve the JSON file for a specific round
@app.route('/round_data/<int:round_number>', methods=['GET'])
@cross_origin()
def serve_round_data(round_number):
    """Serves the JSON file for the specified round"""
    # Construct the filename and path based on the round number
    json_filename = f'round_{round_number}.json'
    json_path = os.path.join(os.getcwd(), 'flask_app', 'create_node_network', 'round_data', json_filename)
    
    # Check if the file exists and serve it
    if os.path.exists(json_path):
        return send_file(json_path, as_attachment=False, mimetype='application/json')
    else:
        return jsonify({"error": f"Round JSON file not found: {json_filename}"}), 404

@app.route('/get_parameters', methods=['GET'])
@cross_origin()
def get_parameters():
    """Fetches the parameters for the Red and Blue teams"""
    global blue_team
    global red_team
    global green_team
    global terminating_conditions

    green_attributes = {
        "size": green_team._size,
        "blue_alignment": green_team._blue_alignment,
        "red_alignment": green_team._red_alignment,
        "neutral": green_team._size - green_team._blue_alignment - green_team._red_alignment
    }
    
    conditions = {
        "population_alignment": terminating_conditions._alignment,
        "round_number": terminating_conditions._round
    }
    
    # TO DO --> currently rounding down - may need to change
    red_team.update_alignment(round(green_team.red_alignment(), 2))
    blue_team.update_alignment(round(green_team.blue_alignment(), 2))

    if blue_team is None or red_team is None: 
        return jsonify({"error": "Parameters not found"}), 404

    output = [red_team.__dict__, blue_team.__dict__, green_attributes, game_style, conditions]
    
    return jsonify(output), 200


# Route to handle UI parameters input
@app.route('/ui_parameters', methods=['POST'])
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

        global terminating_conditions
        terminating_conditions = Termination(parameters['round_number'], parameters['population_alignment'])
        
        if parameters.get('green_node_count_option') == 'random':
            node_count = random.randint(30, 50)  # Adjust the range as needed
            node_attributes, node_connections = generate_random_network(node_count)
        
        elif parameters.get('green_node_count_option') == 'userInput':
            node_count = parameters.get('green_nodes_count')
            connections_per_node = parameters.get('connections_per_node', 3)  # Default to 3 connections per node
            node_attributes, node_connections = generate_user_input_network(node_count, connections_per_node)

        # Already handled in "import_excel"
        elif parameters.get('green_node_count_option') == 'userData':
            return '', 200
        
        else:
            return jsonify({"error": "Invalid green_node_count_option"}), 400

        network_graph=create_node_network(node_attributes, node_connections)
        blue_alignment, red_alignment=convert_alignment_to_node_count(network_graph, red_team._alignment, blue_team._alignment)
        green_team=GreenTeam(network_graph, blue_alignment,red_alignment)

        return jsonify({"message": "Network generated successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to set game play style (continuously or in turns)
@app.route('/set_gameplay', methods=['POST'])
@cross_origin()
def set_gameplay():
    try:
        global game_style
        global red_team
        global blue_team
        global green_team

        data = request.get_json()
        game_style = data['play_option']

        if game_style == "continuous":
            global continuous_game
            continuous_game = Simulation(red_team, blue_team, green_team)

        return '', 200
    
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route('/excel_export', methods=['GET'])
@cross_origin()
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
@app.route('/next_round', methods=['GET'])
@cross_origin()
def start_next_round():
    global turn_counter
    global green_team
    global red_team
    global blue_team

    turn_data = GameTurnData()
    turn_counter = turn_counter + 1
    termination_reason = None
    victor = None
    energy_level = 'NA'


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


    # Temporarily replace the model ID if it is custom
    original_model_id = current_team._model_ID
    if current_team._model_ID == 'custom':
        current_team._model_ID = 'gpt-3.5-turbo'

    current_team.generate_message()

    # Apply penalty to potency of red team message
    if current_team._team.lower() == 'red':
        current_team.apply_penalty()

    # Update green network
    if (not isinstance(current_team._potency, str)):
        green_team.broadcast_message(current_team._potency, current_team._team, current_team._influence_factor)
        green_team.update_green_network()

        # Add the new function to create and save a JSON file for the current round
        create_round_json(turn_counter, green_team._network_graph)

    # Update energy level if the current team is blue
    if current_team._team.lower() == 'blue':
        energy_cost = current_team.energy_cost()
        current_team.update_energy_level(energy_cost)
        energy_level = current_team._energy

    #TODO: currently rounding down - may need to change
    red_team.update_alignment(round(green_team.red_alignment(), 2))
    blue_team.update_alignment(round(green_team.blue_alignment(), 2))
    print(f'Current team has alignment {current_team._alignment}%')
    # Winning by majority support
    if red_team._alignment >= terminating_conditions._alignment:
        victor = red_team._team
        termination_reason = "Majority support for red team"
    elif blue_team._alignment >= terminating_conditions._alignment:
        victor = blue_team._team
        termination_reason = "Majority support for blue team"
    
    # Winning by energy loss
    if current_team._team.lower() == 'blue' and current_team._energy == 0:
        victor = 'Red'
        termination_reason = "Blue team energy depletion"

    # Termination from set round
    if turn_counter == terminating_conditions._round:
        termination_reason = "Round limit reached"
        
    msg_content = {
        "message": current_team._message,
        "potency": current_team._potency,
        "victor": victor,
        "red_team": red_team.__dict__,
        "blue_team": blue_team.__dict__,
        "termination_reason": termination_reason
    }

    turn_data.set_all_turn_data(turn=turn_counter, 
                                team=current_team._team, message_chosen=current_team._message, 
                                potency=current_team._potency, energy_level=energy_level, 
                                red_alignment=green_team.red_alignment(), blue_alignment=green_team.blue_alignment())
    game_data.add_entry(turn_data)

    return jsonify(msg_content), 200

def create_round_json(round_number, network_graph):
    """Creates a JSON file for the network graph for the given round"""
    # Convert the graph to node-link data format
    graph_data = nx.node_link_data(network_graph)
    
    # Define the path to save the JSON file (e.g., round_1.json, round_2.json)
    json_filename = f'round_{round_number}.json'
    json_path = os.path.join(os.getcwd(), 'flask_app', 'create_node_network', 'round_data', json_filename)

    # Ensure the 'round_data' directory exists
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    # Save the graph data to the JSON file
    try:
        with open(json_path, 'w') as f:
            json.dump(graph_data, f, indent=4)
        print(f"Round {round_number} JSON file successfully created at: {json_path}")
    except Exception as e:
        print(f"Failed to save Round {round_number} JSON file: {str(e)}")


# Route to serve continuous gameplay request from the frontend
@app.route('/continuous_game', methods=['GET'])
@cross_origin()
def continuous_game():
    '''Runs a single round of the simulation when playing continuously'''
    try: 
        global continuous_game
        global game_data
        global turn_counter
        global terminating_conditions
        turn_data = GameTurnData()
        
        if continuous_game._termination_reason is None:
            turn_counter += 1
            victor, termination_reason = continuous_game.next_round(terminating_conditions)

            # Add the new function to create and save a JSON file for the current round
            create_round_json(turn_counter, continuous_game._green_team._network_graph)
            
            # Custom round limit
            if  turn_counter == terminating_conditions._round and termination_reason is None:
                termination_reason = "Round limit reached"
            
            current_team = None
            if continuous_game._current_team == "red":
                current_team = continuous_game._red_team
                energy_level = "NA"
            else:
                current_team = continuous_game._blue_team
                energy_level = current_team._energy
            
            msg_content = {
                "message": current_team._message,
                "potency": current_team._potency,
                "red_team": continuous_game._red_team.__dict__,
                "blue_team": continuous_game._blue_team.__dict__,
                "termination_reason": termination_reason,
                "victor": victor,
            }
            turn_data.set_all_turn_data(turn=turn_counter, 
                                team=current_team._team, message_chosen=current_team._message, 
                                potency=current_team._potency, energy_level=energy_level, 
                                red_alignment=green_team.red_alignment(), blue_alignment=green_team.blue_alignment())
            game_data.add_entry(turn_data)

            continuous_game.switch_teams()
            
            return jsonify(msg_content), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Route for cleanup script
@app.route('/cleanup', methods=['GET'])
def cleanup():
    global turn_counter
    global game_data 
    global red_team
    global blue_team
    global green_team
    global custom_llms
    global game_style
    global continuous_game
    global terminating_conditions
    
    try:
        game_data = GameData()  
        turn_counter = 0
        red_team = None
        blue_team = None
        green_team = None
        custom_llms = {}  # Placeholder to store custom LLMs
        game_style = None
        continuous_game = None
        terminating_conditions = None
    
        #Run cleanup script
        subprocess.run('./cleanup.sh')
        return '', 200
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500
        
    

if __name__ == '__main__':
    #game_data = generate_game_data()  # Testing purposes
    app.run(debug=True)