from flask import Flask, jsonify, request
from policy_management import PolicyManager
from logs_management import LogsManager
from ai_integration import analyze_traffic

app = Flask(__name__)

# Instantiate managers
policy_manager = PolicyManager()
logs_manager = LogsManager()

@app.route('/api/get_policy', methods=['GET'])
def get_policy():
    """
    API to get the latest firewall policy for an endpoint.
    """
    policy = policy_manager.get_latest_policy()
    return jsonify(policy)

@app.route('/api/update_policy', methods=['POST'])
def update_policy():
    """
    API to update firewall policy from the admin dashboard.
    """
    new_policy = request.json
    policy_manager.update_policy(new_policy)
    return jsonify({"status": "success"})

@app.route('/api/analyze_traffic', methods=['POST'])
def analyze_traffic_logs():
    """
    API to analyze traffic logs sent by agents.
    """
    traffic_logs = request.json['traffic_logs']
    anomalies = analyze_traffic(traffic_logs)
    logs_manager.store_logs(traffic_logs, anomalies)
    return jsonify(anomalies)

@app.route('/api/get_logs', methods=['GET'])
def get_logs():
    """
    API to get network logs and anomalies for the dashboard.
    """
    logs = logs_manager.get_logs()
    return jsonify(logs)

if __name__ == "__main__":
    app.run(debug=True)
