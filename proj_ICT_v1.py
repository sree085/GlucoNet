from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load the model and the scaler
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            # Extract data from form
            pregnancies = int(request.form["pregnancies"])
            glucose = int(request.form["glucose"])
            bloodpressure = int(request.form["bloodpressure"])
            bmi = float(request.form["bmi"])
            dpf = float(request.form["dpf"])
            age = int(request.form["age"])

            # Combine into a numpy array
            input_data = np.array([[pregnancies, glucose, bloodpressure, bmi, dpf, age]])

            # Apply scaling
            input_scaled = scaler.transform(input_data)

            # Predict using the scaled input
            prediction = model.predict(input_scaled)[0]

            # Format result
            result = "Diabetic" if prediction == 1 else "Not Diabetic"

            return render_template("predict.html", prediction=result)

        except Exception as e:
            return render_template("predict.html", prediction=f"Error: {str(e)}")

    return render_template("predict.html", prediction=None)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
