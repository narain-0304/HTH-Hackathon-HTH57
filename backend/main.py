from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from classify import ensemble_classify
from symptoms import confirm_disease_with_symptoms, process_user_responses
from severity import estimate_severity
from out_of_class import detect_unknown_disease
from py_ai import py_ai_main

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload directory exists
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

file_path = None

@app.route("/api/status", methods=["GET"])
def status():
    """Check if the backend is running."""
    return jsonify({"status": "online"}), 200

@app.route("/api/upload", methods=["POST"])
def upload_file():
    """Handles image upload, classification, and severity estimation."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save the image
    global file_path
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Step 1: Classify Disease (Get top 3 predictions)
    top_3_predictions = ensemble_classify(file_path)
    print("Top 3 Predictions:", top_3_predictions)

    # Step 2: Check if the disease is out of class
    if detect_unknown_disease(top_3_predictions) != True:
        return jsonify({"message": "Unknown disease detected."})

    # Step 3: Ask symptom-related questions
    questions = confirm_disease_with_symptoms(top_3_predictions)
    
    return jsonify({"questions": questions})

@app.route("/api/confirm_symptoms", methods=["POST"])
def confirm_symptoms():
    """Receives user input and finalizes disease classification."""
    data = request.json
    # confirmed_disease = process_user_responses(data["answers"])
    confirmed_disease, severity = process_user_responses(data["answers"])
    
    # Step 4: Estimate severity
    global file_path
    # severity = estimate_severity(file_path, confirmed_disease)
    print("Confirmed Disease:", confirmed_disease)
    print("Estimated Severity:", severity)

    return jsonify({
        "disease": confirmed_disease,
        "severity": severity,
        "message": f"Disease: {confirmed_disease}, Severity: {severity}"
    })

@app.route("/api/get_disease_info", methods=["POST"])
def get_disease_info():
    """Receives disease details and location, calls AI, and returns results."""
    data = request.json
    confirmed_disease = data.get("disease")
    severity = data.get("severity")
    location = data.get("location")

    if not confirmed_disease or not severity or not location:
        return jsonify({"error": "Missing required fields."}), 400
    
    # If severity is "Out of Class", return response immediately
    if severity == "Out of Class":
        return jsonify({"out_of_class": True})

    print(f"Fetching AI info for Disease: {confirmed_disease}, Severity: {severity}, Location: {location}")

    # Call AI only for valid diseases
    ai_results = py_ai_main(confirmed_disease, severity, location)
    print("AI Response:", ai_results)

    return jsonify(ai_results)

if __name__ == "__main__":
    app.run(debug=True, port=5000)


# "Cellulitis", "Impetigo", "Ringworm", "Cutaneous-larva-migrans", "Chickenpox", "Shingles"