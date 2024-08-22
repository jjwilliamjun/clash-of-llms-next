import datetime
from turtle import pd
from flask import Flask, send_file, jsonify
from flask_cors import CORS
from io import BytesIO
from excel_export import *

app = Flask(__name__)
game_data = None #This needs to be a global variable 
CORS(app)

@app.route('/excel_api/export_excel', methods=['GET'])
def export_excel():
    try:
        if game_data is None:
            return jsonify({"error": "No game data available"}), 400

        excel_file =export_data_excel(game_data)

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

if __name__ == '__main__':
    game_data = generate_game_data() #Testing purposes
    app.run(debug=True)
