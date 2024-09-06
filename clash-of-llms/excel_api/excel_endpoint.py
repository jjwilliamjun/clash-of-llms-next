import os
import datetime
from flask import Flask, send_file, jsonify, request
from flask_cors import CORS, cross_origin
import json
import random  # Import for random functionality
from excel_export import *
from import_excel import *
from class_api import team
from set_parameters import *
from create_node_network.create_network import create_node_network, generate_random_network, generate_user_input_network

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Global variables to store game data and team settings
game_data = None  
red_team = None
blue_team = None

@app.route('/excel_api/export_excel', methods=['GET'])
def export_excel():
    """Exports game data to Excel"""
    try:
        if game_data is None:
            return jsonify({"error": "No game data available"}), 400

        excel_file = export_data_excel(game_data)

        if excel_file is None:
            return jsonify({"error": "Failed to generate the Excel file"}), 500
        
        now = datetime.now()
        timestamp = now.strftime("%H_%M_%S")
        excel_file_name = f"clash_of_llms_{timestamp}.xlsx"

        return send_file(
            excel_file,
            download_name=excel_file_name,
            as_attachment=True,   
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/excel_api/excel_import', methods=['POST'])
@cross_origin()
def import_excel():
    """Handles the import of Excel files or random generation of network data"""
    node_attributes = None
    node_connections = None

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

            # Ensure both node_attributes and node_connections are available
            if node_attributes and node_connections:
                # Create the network and save it as a JSON file
                create_node_network(node_attributes, node_connections)
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
            create_node_network(node_attributes, node_connections)
            return jsonify({"message": "Network generated successfully!"}), 200
        
        else:
            return jsonify({"error": "No files or valid JSON provided"}), 400

    except Exception as e:
        print(f"Error during file upload: {e}")
        return jsonify({"error": str(e)}), 500



# Route to serve network_output.json
@app.route('/network_output.json', methods=['GET'])
def serve_network_output():
    """Serves the network output JSON file"""
    json_path = os.path.join(os.path.dirname(__file__), 'create_node_network', 'network_output.json')
    if os.path.exists(json_path):
        return send_file(json_path, as_attachment=False, mimetype='application/json')
    else:
        return jsonify({"error": "JSON file not found"}), 404

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

        create_node_network(node_attributes, node_connections)
        return jsonify({"message": "Network generated successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return '', 200

# Route to serve next round request from the frontend
@app.route('/excel_api/next_round', methods=['GET'])
@cross_origin()
def start_next_round():
    msg_content = []
    
    team_colour = request.args.get('team')

    if blue_team is None or red_team is None: 
        return jsonify({"error": "Team not found"}), 404
    
    if team_colour == 'red':
        current_team = red_team
    elif team_colour == 'blue':
        current_team = blue_team
    else:
        return jsonify({"error": "Incorrect team colour"}), 404
    
    current_team.generate_message()
    msg_content.append(current_team._message)
    msg_content.append(current_team._potency)
        
    return jsonify(msg_content), 200

if __name__ == '__main__':
    game_data = generate_game_data()  # Testing purposes
    app.run(debug=True)
