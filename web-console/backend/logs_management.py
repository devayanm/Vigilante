import json
from models.logs_model import LogsModel

class LogsManager:
    def __init__(self):
        self.logs_model = LogsModel()

    def store_logs(self, traffic_logs, anomalies):
        """
        Store traffic logs and anomalies in the database.
        """
        logs_json = json.dumps(traffic_logs)
        anomalies_json = json.dumps(anomalies)
        self.logs_model.store_logs(logs_json, anomalies_json)

    def get_logs(self):
        """
        Retrieve logs and anomalies from the database.
        """
        return self.logs_model.get_logs()
