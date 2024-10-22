from flask import Flask, jsonify, request, render_template
import pandas as pd
import os

app = Flask(__name__)

# Load the Excel file directly from the code
excel_file = 'data.xlsx'  # Assuming the file is in the same directory

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_sheets', methods=['GET'])
def get_sheets():
    try:
        xls = pd.ExcelFile(excel_file)
        sheet_names = xls.sheet_names
        return jsonify({"sheet_names": sheet_names})
    except Exception as e:
        print(f"Error reading sheets: {e}")
        return jsonify({"error": "Error reading sheets"}), 500

@app.route('/get_options', methods=['POST'])
def get_options():
    data = request.get_json()
    sheet_name = data.get('sheet_name')

    try:
        xls = pd.ExcelFile(excel_file)
        df = pd.read_excel(xls, sheet_name)

        # Adjust ranges based on the sheet
        if sheet_name == "صحيح":
            options = df.iloc[6:26, 15].dropna().unique().tolist()  # P7:P26
        elif sheet_name == "اجوف":
            options = df.iloc[6:17, 15].dropna().unique().tolist()  # P7:P17
        elif sheet_name == "ناقص":
            options = df.iloc[6:15, 15].dropna().unique().tolist()  # P7:P15
        elif sheet_name == "مضاعف":
            options = df.iloc[6:11, 15].dropna().unique().tolist()  # P7:P11
        else:
            options = []

        return jsonify({"options": options})
    except Exception as e:
        print(f"Error reading options: {e}")
        return jsonify({"error": "Error reading options"}), 500

@app.route('/update_table', methods=['POST'])
def update_table():
    data = request.get_json()
    sheet_name = data.get('sheet_name')
    selected_value = data.get('selected_value')

    try:
        xls = pd.ExcelFile(excel_file)
        df = pd.read_excel(xls, sheet_name)

        # Update G6 cell with the selected dropdown value
        df.iloc[5, 6] = selected_value

        # Retrieve the updated table from A5:E20
        updated_table = df.iloc[4:20, 0:5].values.tolist()

        return jsonify(updated_table)
    except Exception as e:
        print(f"Error updating table: {e}")
        return jsonify({"error": "Error updating table"}), 500

if __name__ == '__main__':
    app.run(debug=True)
