
import pandas as pd
import numpy as np
import random
import time
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Simulating CAN bus message data
def generate_can_data(num_samples=1000):
    data = []
    for _ in range(num_samples):
        timestamp = time.time()
        message_id = random.choice([0x100, 0x200, 0x300, 0x666])  # Some normal & one malicious ID
        dlc = random.randint(0, 8)  # Data length
        message_frequency = random.randint(1, 100)  # Frequency of message
        data.append([timestamp, message_id, dlc, message_frequency])

    df = pd.DataFrame(data, columns=["timestamp", "message_id", "dlc", "message_frequency"])
    df.to_csv("can_messages.csv", index=False)
    print("? CAN Data saved to can_messages.csv")
    return df

# Train the Isolation Forest model
def train_model():
    df = generate_can_data(1000)

    # Selecting only numerical features for training
    X = df[["message_frequency"]]

    # Standardizing the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Training Isolation Forest
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X_scaled)

    # Saving the model and scaler
    joblib.dump({"model": model, "features": X.columns.tolist()}, "isolation_forest_model.pkl")
    joblib.dump(scaler, "scaler.pkl")

    print("? Model trained & saved as isolation_forest_model.pkl")

if __name__ == "__main__":
    train_model()
