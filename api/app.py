import os
import random
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the data folder where CSVs are stored
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")

# Define CSV files with correct paths
tech_csv_files = {
    "softwaredeveloper": os.path.join(DATA_FOLDER, "software_developer.csv"),
    "dataanalyst": os.path.join(DATA_FOLDER, "data_analyst.csv"),
    "aimlengineer": os.path.join(DATA_FOLDER, "ai_ml_engineer.csv"),
    "developerengineer": os.path.join(DATA_FOLDER, "developer_engineer.csv"),
    "cloudengineer": os.path.join(DATA_FOLDER, "cloud_engineer.csv")
}

non_tech_csv_files = [
    os.path.join(DATA_FOLDER, "teamwork.csv"),
    os.path.join(DATA_FOLDER, "communication.csv"),
    os.path.join(DATA_FOLDER, "leadership.csv"),
    os.path.join(DATA_FOLDER, "problem_solving.csv"),
    os.path.join(DATA_FOLDER, "adaptability.csv"),
    os.path.join(DATA_FOLDER, "time_management.csv"),
    os.path.join(DATA_FOLDER, "conflict_resolution.csv"),
    os.path.join(DATA_FOLDER, "ethics.csv"),
    os.path.join(DATA_FOLDER, "career_development.csv"),
    os.path.join(DATA_FOLDER, "customer_service.csv"),
    os.path.join(DATA_FOLDER, "creativity.csv")
]

# Function to load CSV files
def load_csv(file_name):
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        raise FileNotFoundError(f"File {file_name} not found!")

@app.route('/get-questions', methods=['GET', 'POST'])
def get_questions():
    try:
        # Get role from query parameters
        role = request.args.get("role", "").lower()

        if role not in tech_csv_files:
            return jsonify({"error": "Invalid role"}), 400

        # Load technical questions
        tech_df = load_csv(tech_csv_files[role])
        tech_df.fillna("N/A", inplace=True)  # Replacing NaN values
        tech_questions = tech_df.sample(n=random.randint(3, 5)).to_dict(orient='records')

        # Load non-technical questions
        non_tech_questions = []
        selected_files = random.sample(non_tech_csv_files, random.randint(3, 5))

        for file in selected_files:
            df = load_csv(file)
            df.fillna("N/A", inplace=True)  # Replacing NaN values
            if not df.empty:
                question = df.sample(n=1).to_dict(orient='records')[0]
                non_tech_questions.append(question)

        # Combine and shuffle questions (Tech first, then Non-Tech)
        combined_questions = tech_questions + non_tech_questions

        return jsonify(combined_questions), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
