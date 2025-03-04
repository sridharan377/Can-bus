import can
import pandas as pd
import time

# Configure CAN interface
bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

# Initialize empty list to store messages
data_records = []

print(" Logging CAN Bus messages... Press Ctrl+C to stop.")

twry:
    while True:
        msg = bus.recv(timeout=5)  # Timeout added to avoid infinite blocking
        if msg is None:
            print("?? No message received in the last 5 seconds.")
            continue

        timestamp = time.time()
        data_dec = int(msg.data.hex(), 16) if msg.data else 0

        # Print message for debugging
        print(f"? Received: ID={hex(msg.arbitration_id)}, DATA={msg.data.hex()}, TIMESTAMP={timestamp}")

        # Store data
        data_records.append({"ID": msg.arbitration_id, "DATA_DEC": data_dec, "TIMESTAMP": timestamp})

except KeyboardInterrupt:
    if data_records:
        df = pd.DataFrame(data_records)
        df.to_csv("can_data.csv", index=False)
        print("\n? CAN messages saved to 'can_data.csv'.")
    else:
        print("\n?? No CAN messages received. Check your setup!")
