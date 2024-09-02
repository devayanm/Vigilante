import sqlite3

class PolicyModel:
    def __init__(self):
        self.connection = sqlite3.connect('firewall.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS policies (id INTEGER PRIMARY KEY, policy TEXT)''')

    def get_policy(self):
        """
        Get the latest firewall policy from the database.
        """
        self.cursor.execute("SELECT policy FROM policies ORDER BY id DESC LIMIT 1")
        policy = self.cursor.fetchone()
        return policy[0] if policy else None

    def update_policy(self, policy):
        """
        Insert a new firewall policy into the database.
        """
        self.cursor.execute("INSERT INTO policies (policy) VALUES (?)", (policy,))
        self.connection.commit()
