from flask import Flask, request, jsonify
from flask_cors import CORS  
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

model = joblib.load("best_yield_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoder = joblib.load("label_encoder.pkl")

required_fields = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'ph', 'rainfall']

@app.route("/predict", methods=["POST"])
def predict_crop():
    data = request.get_json()
    required_fields = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'ph', 'rainfall', 'crop']
    
    if not all(field in data and data[field] != "" for field in required_fields):
        return jsonify({"error": "Missing one or more required input fields."}), 400

    try:
        input_values = [float(data[field]) for field in ['temperature', 'rainfall', 'humidity', 'ph', 'nitrogen', 'phosphorus', 'potassium']]
        crop_name = data['crop'].strip().lower()

        all_crops_lower = [c.lower() for c in label_encoder.classes_]
        if crop_name not in all_crops_lower:
            return jsonify({"error": f"Invalid crop name: {crop_name}"}), 400

        crop_encoded = label_encoder.transform([label_encoder.classes_[all_crops_lower.index(crop_name)]])[0]

        scaled_input = scaler.transform([input_values])
        final_input = np.hstack([scaled_input, [[crop_encoded]]])

        predicted_yield = model.predict(final_input)[0]
        return jsonify({"prediction": f"{predicted_yield:.2f} tons/ha"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def recommend_best_crop(data):
    """
    Recommend the best crop based on soil and climate conditions.
    Returns the crop name and expected yield.
    """
    try:
        input_values = [float(data[field]) for field in ['temperature', 'rainfall', 'humidity', 'ph', 'nitrogen', 'phosphorus', 'potassium']]
        
        all_crops = label_encoder.classes_
        
        best_yield = -1
        best_crop = None
      
        for crop in all_crops:
            crop_encoded = label_encoder.transform([crop])[0]
            
            scaled_input = scaler.transform([input_values])
            final_input = np.hstack([scaled_input, [[crop_encoded]]])
            
            predicted_yield = model.predict(final_input)[0]
            
            if predicted_yield > best_yield:
                best_yield = predicted_yield
                best_crop = crop
        
        return best_crop, round(best_yield, 2)
        
    except Exception as e:
        raise Exception(f"Recommendation calculation failed: {str(e)}")


@app.route("/recommend", methods=["POST"])
def recommend_crop():
    data = request.get_json()
    

    if not all(field in data and data[field] != "" for field in required_fields):
        return jsonify({"error": "Missing one or more required input fields"}), 400
    
    try:
        best_crop, expected_yield = recommend_best_crop(data)
        return jsonify({
            "recommended_crop": best_crop,
            "expected_yield": f"{expected_yield} tons/ha"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
