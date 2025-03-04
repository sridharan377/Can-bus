import random
import can
import time
import logging
import csv
import smtplib
from email.mime.text import MIMEText
from flask import Flask
from flask_socketio import SocketIO, emit
from threading import Thread
import joblib
import numpy as np
import traceback
import pandas as pd
from influxdb_client import InfluxDBClient, Point, WriteOptions, WritePrecision

logging.basicConfig(filename ="backend.log", level= logging.DEBUG,format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

CAN_INTERFACE = "vcan0"
model_data = joblib.load("isolation_forest_model.pkl")
ml_model = model_data["model"]
feature_names = model_data["features"]
scaler = joblib.load("scaler.pkl")

INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "your_influxdb_token"
INFLUXDB_ORG ="can_project"
INFLUXDB_BUCKET = "can_data"

client = InfluxDBClient(url = INFLUXDB_URL, token = INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=1000))

NORMAL_MESSAGES = [
    can.Message(arbitration_id=0x100, data=[0x01, 0x02, 0x03, 0x04], is_extended_id=False),
    can.Message(arbitration_id=0x200, data=[0x05, 0x06, 0x07, 0x08], is_extended_id=False),
]

MALICIOUS_MESSAGES = [
    can.Message(arbitration_id=0x666, data=[0xFF, 0xFF, 0xFF, 0xFF], is_extended_id=False),
]

# Store timestamps and message counts
message_data = {"timestamps": [], "counts": []}



MESSAGE_RATE_THRESHOLD = 100
UNUSUAL_IDS = {0x666, 0xDEAD, 0xBEEF}
PREVIOUS_ID = None
message_counter ={}
anomalies = []
#Alerting Funcation



def send_alert(message):
    try:
        sender_email = "your-email@gmail.com"
        recipient_email = "admin@example.com"
        msg = MIMEText(message)
        msg["Subject"] = "CAN Bus Anomaly Detection"
        msg["From"] = sender_email
        msg["To"] = recipient_email
        
        server= smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, "your-email-password")
        server.sendmail(sender_email, recipient_email,msg.as_string())
        server.quit()
        logging.info("Alert email sent.")
    except Exception as e:
        logging.error(f"Failed to send alert: {e}")
        

def send_can_messages():
    global PREVIOUS_ID
    try:
        bus = can.interface.Bus(channel=CAN_INTERFACE, interface='socketcan')
        logging.info("CAN interface initialized successfully.")
    except Exception as e:
        print("Error accessing CAN interface:", e)
        logging.error(f"Error accessing CAN interface: {e}")
        return

    while True:
        msg = random.choice(NORMAL_MESSAGES + MALICIOUS_MESSAGES)
        timestamp = time.strftime("%H:%M:%S")
        message_id = msg.arbitration_id
        data_payload = msg.data.hex()
        message_frequency = random.randint(1, 100)
        message_counter[message_id] = message_counter.get(message_id, 0)+ 1
        anomaly_score = ml_model.predict(pd.DataFrame([[message_frequency]], columns=feature_names).to_numpy())[0]
        is_anomalous = anomaly_score == -1
        
        if is_anomalous:
            anomaly_message = f" ML-detected anomaly: ID {hex(message_id)}, Freq {message_frequency}"
            anomalies.append(anomaly_message)
            logging.warning(anomaly_message)
            send_alert(anomaly_message)
            with open("anomaly_log.csv", "a") as log_file:
                log_file.write(f"{timestamp}, {hex(message_id)}, ML Detected Anomaly\n")
        try:
            timestamp = time.time()  # Get the current timestamp
            is_extended = msg.is_extended_id  # Check if it's a standard or extended ID
            crc = random.randint(0, 65535)  # Simulated CRC value
            ack = True  # Simulating successful message reception
            rtr = msg.is_remote_frame  # Remote Transmission Request flag
            dlc = msg.dlc  # Data Length Code
            data_payload = msg.data.hex()  # Convert data to hex string
            
            # Bus Load and Message Frequency (simulated for now)
            bus_load = random.uniform(10, 90)  # Fake percentage for bus load
            message_frequency = message_counter.get(message_id, 0)  # Simulated frequency count
            
            
            
            message_counter[message_id] = message_counter.get(message_id, 0) + 1
            if message_counter[message_id] > MESSAGE_RATE_THRESHOLD:
                anomaly = f"High message rate detected fro ID { hex(message_id)}"
                anomalies.append(anomaly)
                logging.warning(anomaly)
                send_alert(anomaly)
            if message_id not in UNUSUAL_IDS:
                anomaly = f"Unusual CAN ID detected: {hex(message_id)}"
                anomalies.append(anomaly)
                logging.warning(anomaly)
                with open("anomaly_log.csv", "a") as log_file:
                    log_file.write(f"{time.time()},{hex(message_id)},Unusal CAN ID\n")
                send_alert(anomaly)

            if PREVIOUS_ID and message_id < PREVIOUS_ID:
                anomaly = f"Out-of-sequence message detected: {hex(message_id)} after {hex(PREVIOUS_ID)}"
                anomalies.append(anomaly)
                logging.warning(anomaly)
                send_alert(anomaly)
                PREVIOUS_ID = message_id
                
            if anomaly_score == -1:
                anomaly = f"ML Detected Anomaly: ID = {hex(message_id)}, Frequency={message_frequency}"
                anomalies.append(anomaly)
                logging.warning(anomaly)
                send_alert(anomaly)
                
            timestamp_ns = int(time.time() * 1e9)
            
            #store data in InfluxDB
            point = Point("can_message") \
                .time(timestamp_ns, WritePrecision.NS) \
                .field("message_id", message_id) \
                .field("message_frequency", message_frequency) \
                .field("bus_load", bus_load) \
                .field("anomaly_detected", 1) \
                .field("is_anomalous", int(is_anomalous))

            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

            
            socketio.emit('new_message', {
                'timestamp': timestamp,
                'id': hex(msg.arbitration_id),
                'is_extended': is_extended,
                'dlc': dlc,
                'data': data_payload,
                'crc': crc,
                'ack': ack,
                'rtr': rtr,
                'bus_load': bus_load,
                'message_frequency': message_frequency,
            })
            
            if anomalies:
                with open("anomaly_log.csv", "a") as log_files:
                    writer = csv.writer(log_files)
                    for anomaly in anomalies:
                        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), anomaly])
                    anomalies.clear()
            
            logging.info(f"Sent CAN message: ID={hex(message_id)}, Data={data_payload}")
        


            logging.info(f"Sent CAN message: ID={hex(msg.arbitration_id)}, Data={data_payload}")
            time.sleep(1)

            # Update graph data
            current_time = time.strftime("%H:%M:%S")
            if len(message_data["timestamps"]) > 10:
                message_data["timestamps"].pop(0)
                message_data["counts"].pop(0)

            message_data["timestamps"].append(current_time)
            message_data["counts"].append(len(message_data["timestamps"]))

            socketio.emit("update_graph", message_data)
            time.sleep(1)
        except Exception as e:
            print("Error sending CAN message:", e)
            logging.error(f"Error sending CAN message: {e}")
            print(traceback.format_exc())
            
            
@app.route("/")       
def home():
    return "CAN Bus Backend is Running"

if __name__ == "__main__":
    logging.info("Starting backend service ..")
    can_thread = Thread(target=send_can_messages)
    can_thread.daemon = True
    can_thread.start()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

