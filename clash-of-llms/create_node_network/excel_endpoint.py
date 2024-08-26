import os
import datetime
from flask import Flask, send_file, jsonify, request
from flask_cors import CORS, cross_origin
import json
from excel_export import *
from import_excel import *

app = Flask(__name__)
game_data = None  # This needs to be a global variable
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/excel_api/export_excel', methods=['GET'])
def export_excel():
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

@app.route('/excel_api/excel_import', methods=['GET', 'POST'])
@cross_origin()
def import_excel():
    output = []

    if request.method == 'POST':

        for key, file_storage in request.files.items(multi=True):
            file = request.files[f"{key}"]
            file_path = os.path.join('/tmp', file.filename)
            file.save(file_path)

            if key == 'settings_file':
                settings = import_settings(file_path)
                output.append(settings[0].to_dict())
                output.append(settings[1].to_dict())
            elif key == 'attributes_file':
                nodes = import_node_attributes(file_path)
                output.append(nodes)
            elif key == 'connections_file':
                connections = import_node_connections(file_path)
                output.append(connections)

    return jsonify(output)

# Route to serve network_output.json
@app.route('/network_output.json', methods=['GET'])
def serve_network_output():
    json_path = os.path.join(os.path.dirname(__file__), 'network_output.json')
    if os.path.exists(json_path):
        return send_file(json_path, as_attachment=False, mimetype='application/json')
    else:
        return jsonify({"error": "JSON file not found"}), 404

if __name__ == '__main__':
    game_data = generate_game_data()  # Testing purposes
    app.run(debug=True)
