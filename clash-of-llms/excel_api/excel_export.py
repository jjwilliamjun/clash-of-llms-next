"""Uses pandas to export data using a dataframe"""
from io import BytesIO
import pandas as pd
from openpyxl import load_workbook
from game_data import GameData, GameTurnData

def export_data_excel(simulation_data_list):
    """Saving file using pd dataframe"""
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

    except (OSError, TypeError) as error:
        print(f"An error occurred while saving the Excel file: {error}")
        return None

def generate_game_data():
    """Test generating game data"""
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


def set_col_width(excel_file):
    """Setting column width for excel file"""
    workbook = load_workbook(filename=excel_file)
    worksheet = workbook.active

    for column_cells in worksheet.columns:
        max_length = 0
        column = column_cells[0].column_letter

        for cell in column_cells:
            try:
                max_length = max(max_length, len(str(cell.value)))
            except (TypeError, AttributeError):
                pass

        adjusted_width = max_length + 2
        worksheet.column_dimensions[column].width = adjusted_width

    # Save the workbook
    workbook.save(filename=excel_file)
