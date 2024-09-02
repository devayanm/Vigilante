import json
import requests

class TrafficLogger:
    def __init__(self, log_file='traffic_logs.json'):
        self.log_file = log_file

    def log_traffic(self, traffic_data):
        """
        Log network traffic data to a local file.
        """
        with open(self.log_file, 'a') as file:
            json.dump(traffic_data, file)
            file.write('\n')

    def send_logs_to_server(self, traffic_data):
        """
        Send traffic logs to the central web console for anomaly detection.
        """
        url = 'http://<web-console-server>/api/analyze_traffic'
        response = requests.post(url, json={'traffic_logs': traffic_data})
        if response.status_code == 200:
            print("Logs sent successfully")
        else:
            print("Failed to send logs")

if __name__ == "__main__":
    logger = TrafficLogger()
    sample_data = {
        "app_name": "chrome",
        "local_ip": "192.168.1.2",
        "remote_ip": "172.217.12.46",
        "protocol": "TCP",
        "local_port": 443,
        "remote_port": 80
    }
    logger.log_traffic(sample_data)
    logger.send_logs_to_server(sample_data)
