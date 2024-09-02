import requests

def analyze_traffic(traffic_logs):
    """
    Send traffic logs to the AI/ML backend for anomaly detection.
    """
    url = 'http://localhost:5000/api/analyze_traffic'  # Point to the AI/ML backend
    response = requests.post(url, json={'traffic_logs': traffic_logs})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to analyze traffic"}
