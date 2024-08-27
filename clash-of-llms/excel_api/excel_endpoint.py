"""Endpoint that exports to excel"""
from datetime import datetime
from flask import Flask, send_file, jsonify
from flask_cors import CORS
from excel_export import export_data_excel, generate_game_data

app = Flask(__name__)
GAMEDATA = None #This needs to be a global variable
CORS(app)

@app.route('/excel_api/export_excel', methods=['GET'])
def export_excel():
    """Exports to excel"""
    try:
        if GAMEDATA is None:
            return jsonify({"error": "No game data available"}), 400

        excel_file =export_data_excel(GAMEDATA)

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

    except (ImportError, TypeError) as error:
        return jsonify({"error": str(error)}), 500

if __name__ == '__main__':
    game_data = generate_game_data() #Testing purposes
    app.run(debug=True)
