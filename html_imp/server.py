from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import os
import sys
import util

# Get the absolute path to the templates directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=TEMPLATES_DIR)
CORS(app)  # Enable CORS for all routes

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        print("\n=== Received Prediction Request ===")
        print("Request data:", request.get_data())
        data = request.get_json()
        print("Parsed JSON:", data)
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        total_sqft = float(data.get('total_sqft', 0))
        location = data.get('location', '')
        bhk = int(data.get('bhk', 0))
        bath = int(data.get('bath', 0))
        
        print(f"Processing request - Location: {location}, Sqft: {total_sqft}, BHK: {bhk}, Bath: {bath}")

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        response = jsonify({
            'estimated_price': estimated_price
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return response

@app.route('/')
def home():
    return render_template('app.html')

# Serve static files (CSS, JS, etc.)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(TEMPLATES_DIR, filename)

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    print(f"Serving files from: {TEMPLATES_DIR}")
    print("Python version:", sys.version)
    print("Working directory:", os.getcwd())
    
    # Load the model and data
    print("Loading saved artifacts...")
    util.load_saved_artifacts()
    print("Successfully loaded artifacts!")
    
    # Run the app
    print("Starting server on http://127.0.0.1:5000")
    app.run()