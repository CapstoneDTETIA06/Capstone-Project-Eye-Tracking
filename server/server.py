import redis
import time
import json
from threading import Lock
import csv
from collections import deque
from datetime import datetime

class SynchronizedSubscriber:
    def __init__(self, csv_filename, buffer_size=100):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.pubsub = self.redis_client.pubsub()
        self.moving_target_data = None
        self.eye_tracker_data = None
        self.lock = Lock()
        self.csv_filename = csv_filename
        self.data_buffer = deque(maxlen=buffer_size)
        self.last_write_time = time.time()
        self.write_interval = 5  # Write to CSV every 5 seconds

        # Initialize CSV file with headers
        with open(self.csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Timestamp', 'MovingTarget_X', 'MovingTarget_Y', 'EyeTracker_X', 'EyeTracker_Y'])

    def moving_target_handler(self, message):
        if message['type'] == 'message':
            with self.lock:
                self.moving_target_data = message['data'].decode('utf-8')
                if self.eye_tracker_data:
                    self.process_data()
                    self.eye_tracker_data = None  # Reset eye tracker data after processing

    def eye_tracker_handler(self, message):
        if message['type'] == 'message':
            with self.lock:
                self.eye_tracker_data = message['data'].decode('utf-8')

    def process_data(self):
        timestamp = datetime.now().isoformat()
        mt_x, mt_y = self.moving_target_data['x'], self.moving_target_data['y']
        et_x, et_y = self.eye_tracker_data['x'], self.eye_tracker_data['y']
        
        # Add data to buffer
        self.data_buffer.append([timestamp, mt_x, mt_y, et_x, et_y])
        
        # Check if it's time to write to CSV
        current_time = time.time()
        if current_time - self.last_write_time >= self.write_interval:
            self.write_to_csv()
            self.last_write_time = current_time

    def write_to_csv(self):
        if not self.data_buffer:
            return

        with open(self.csv_filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.data_buffer)
        
        self.data_buffer.clear()
        print(f"Data written to {self.csv_filename}")

    def subscribe(self):
        self.pubsub.subscribe(**{
            'MovingTarget': self.moving_target_handler,
            'EyeTracker': self.eye_tracker_handler
        })

    def run(self):
        print(f"Starting synchronized subscriber... Data will be saved to {self.csv_filename}")
        print("Listening for messages... (Ctrl+C to stop)")

        subscription_thread = self.pubsub.run_in_thread(sleep_time=0.001)

        try:
            while True:
                time.sleep(0.1)  # Small sleep to prevent high CPU usage
        except KeyboardInterrupt:
            print("Stopping subscriber...")
            self.write_to_csv()  # Write any remaining data
            subscription_thread.stop()
            print("Subscriber stopped.")

if __name__ == "__main__":
    csv_filename = f"eye_tracking_data_{int(time.time())}.csv"
    subscriber = SynchronizedSubscriber(csv_filename)
    subscriber.subscribe()
    subscriber.run()