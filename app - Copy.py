from flask import Flask, request, jsonify, render_template
import pandas as pd
import os

app = Flask(__name__)

# Path to the Excel file bundled with the application
EXCEL_FILE_PATH = 'data.xlsx'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_sheets', methods=['GET'])
def get_sheets():
    try:
        xls = pd.ExcelFile(EXCEL_FILE_PATH)
        sheet_names = xls.sheet_names
        return jsonify({"sheet_names": sheet_names})
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return jsonify({"error": "Error reading Excel file"}), 500

@app.route('/get_options', methods=['POST'])
def get_options():
    sheet_name = request.json.get('sheet_name')

    try:
        xls = pd.ExcelFile(EXCEL_FILE_PATH)
        df = pd.read_excel(xls, sheet_name)

        # Adjust to get options from specified ranges
        if sheet_name == "صحيح":  # 1st sheet
            options = df.iloc[6:26, 15].dropna().unique().tolist()  # P7:P26
        elif sheet_name == "اجوف":  # 2nd sheet
            options = df.iloc[6:17, 15].dropna().unique().tolist()  # P7:P17
        elif sheet_name == "ناقص":  # 3rd sheet
            options = df.iloc[6:15, 15].dropna().unique().tolist()  # P7:P15
        elif sheet_name == "مضاعف":  # 4th sheet
            options = df.iloc[6:11, 15].dropna().unique().tolist()  # P7:P11
        else:
            options = []  # Default in case of an unknown sheet

        options = [str(opt) for opt in options if pd.notna(opt)]
        return jsonify({"options": options})
    except Exception as e:
        print(f"Error processing sheet: {e}")
        return jsonify({"error": "Error processing sheet"}), 500

@app.route('/update_table', methods=['POST'])
def update_table():
    sheet_name = request.json.get('sheet_name')
    selected_value = request.json.get('selected_value')

    try:
        # Load the Excel file
        xls = pd.ExcelFile(EXCEL_FILE_PATH)
        df = pd.read_excel(xls, sheet_name)

        # Write the selected value to G6 (row index 5, column index 6)
        df.iloc[5, 6] = selected_value

        # Reload the DataFrame to ensure any calculations based on G6 are updated
        df = pd.read_excel(EXCEL_FILE_PATH, sheet_name)

        # Retrieve the updated table from A5:E20
        updated_data = df.iloc[4:20, 0:5].values.tolist()  # A5:E20

        return jsonify(updated_data)
    except Exception as e:
        print(f"Error updating table: {e}")
        return jsonify({"error": "Error updating table"}), 500

if __name__ == '__main__':
    app.run(debug=True)
