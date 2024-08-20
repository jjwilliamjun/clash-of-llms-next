from datetime import datetime
from io import BytesIO
import pandas as pd
from openpyxl import load_workbook
from game_data import GameData, GameTurnData

def export_data_excel(simulation_data_list):
    try:
        df = pd.DataFrame(simulation_data_list.get_results())

        output = BytesIO()

        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            
            worksheet = writer.sheets['Sheet1']
            for i, col in enumerate(df.columns):
                max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, max_len)
        
        output.seek(0) 

        return output

    except Exception as e:
        print(f"An error occurred while saving the Excel file: {e}")
        return None
def generate_game_data():
        game_data = GameData()

        turn_data_1 = GameTurnData()
        turn_data_1.set_turn(1)
        turn_data_1.set_team('Blue')
        turn_data_1.set_message_chosen('Message is true')
        turn_data_1.set_potency(0.8)
        turn_data_1.set_energy_level(80)
        turn_data_1.set_increased_alignment(60)

        game_data.add_entry(turn_data_1)

        turn_data_2 = GameTurnData()
        turn_data_2.set_turn(2)
        turn_data_2.set_team('Red')
        turn_data_2.set_message_chosen('Message is false')
        turn_data_2.set_potency(0.6)
        turn_data_2.set_energy_level(70)
        turn_data_2.set_increased_alignment(40)
        turn_data_2.set_decreased_alignment(10)

        game_data.add_entry(turn_data_2)
        return game_data


def flask_export_test():
    try:
        game_data = GameData()

        # Create and populate GameTurnData instances
        turn_data_1 = GameTurnData()
        turn_data_1.set_turn(1)
        turn_data_1.set_team('Blue')
        turn_data_1.set_message_chosen('Message is true')
        turn_data_1.set_potency(0.8)
        turn_data_1.set_energy_level(80)
        turn_data_1.set_increased_alignment(60)

        # Add the populated turn_data_1 to game_data
        game_data.add_entry(turn_data_1)

        # Create and populate another GameTurnData instance
        turn_data_2 = GameTurnData()
        turn_data_2.set_turn(2)
        turn_data_2.set_team('Red')
        turn_data_2.set_message_chosen('Message is false')
        turn_data_2.set_potency(0.6)
        turn_data_2.set_energy_level(70)
        turn_data_2.set_increased_alignment(40)
        turn_data_2.set_decreased_alignment(10)

        # Add the populated turn_data_2 to game_data
        game_data.add_entry(turn_data_2)
        df = pd.DataFrame(game_data.get_results())

        # Use BytesIO to create an in-memory file
        output = BytesIO()

        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            for i, col in enumerate(df.columns):
                max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, max_len)
        
        output.seek(0) 

        return output

    except Exception as e:
        print(f"An error occurred while saving the Excel file: {e}")
        return None

def set_col_width(excel_file):
    workbook = load_workbook(filename=excel_file)
    worksheet = workbook.active

    for column_cells in worksheet.columns:
        max_length = 0
        column = column_cells[0].column_letter 

        for cell in column_cells:
            try:
                max_length = max(max_length, len(str(cell.value)))
            except:
                pass

        adjusted_width = max_length + 2 
        worksheet.column_dimensions[column].width = adjusted_width

    # Save the workbook
    workbook.save(filename=excel_file)





