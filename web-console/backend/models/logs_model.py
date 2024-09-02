import sqlite3

class LogsModel:
    def __init__(self):
        self.connection = sqlite3.connect('firewall.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, logs TEXT, anomalies TEXT)''')

    def store_logs(self, logs, anomalies):
        """
        Store network logs and detected anomalies in the database.
        """
        self.cursor.execute("INSERT INTO logs (logs, anomalies) VALUES (?, ?)", (logs, anomalies))
        self.connection.commit()

    def get_logs(self):
        """
        Retrieve all logs and anomalies from the database.
        """
        self.cursor.execute("SELECT logs, anomalies FROM logs")
        return self.cursor.fetchall()
