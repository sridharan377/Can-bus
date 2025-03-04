from flask import Flask, jsonify
import can
import joblib
import pandas as pd  # Missing import added
import time

# Load trained ML model
model = joblib.load("can_anomaly_model.pkl")

# Configure Flask API
app = Flask(__name__)

# Configure CAN interface
bus = can.interface.Bus(channel="vcan0", bustype="socketcan")

# Store last timestamp to calculate TIME_DIFF
last_timestamp = None

@app.route("/predict", methods=["GET"])
def predict():
    global last_timestamp  # Needed to update time difference

    msg = bus.recv(timeout=1)  # Add timeout to prevent infinite wait
    if msg is None:
        return jsonify({"error": "No CAN message received"}), 400

    timestamp = time.time()

    # Convert message data
    data_dec = int(msg.data.hex(), 16) if msg.data else 0

    # Calculate TIME_DIFF (difference from the last received message)
    time_diff = timestamp - last_timestamp if last_timestamp else 0
    last_timestamp = timestamp  # Update for next call

    # Create a DataFrame with correct column names
    features = pd.DataFrame([[msg.arbitration_id, data_dec, time_diff]], 
                            columns=["ID", "DATA_DEC", "TIME_DIFF"])

    # Predict anomaly (-1 = Anomaly, 1 = Normal)
    prediction = model.predict(features)

    response = {
        "ID": hex(msg.arbitration_id),
        "DATA": msg.data.hex(),
        "Anomaly": bool(prediction[0] == -1),  # True if anomaly detected
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
