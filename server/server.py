from flask import Flask, request, jsonify, render_template
from . import util  # ✅ fixed import

app = Flask(__name__)

# ✅ Load model artifacts when app starts
util.load_saved_artifacts()

@app.route('/')
def index():
    return render_template('index.html')

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
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

        return jsonify({'estimated_price': estimated_price})
    except Exception as e:
        print("Prediction error:", e)
        return jsonify({'error': str(e)})
