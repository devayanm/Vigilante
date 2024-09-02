import sqlite3

def init_db():
    connection = sqlite3.connect('firewall.db')
    cursor = connection.cursor()

    # Create policies table
    cursor.execute('''CREATE TABLE IF NOT EXISTS policies (
                        id INTEGER PRIMARY KEY,
                        policy TEXT)''')

    # Create logs table
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY,
                        logs TEXT,
                        anomalies TEXT)''')

    connection.commit()
    connection.close()

if __name__ == "__main__":
    init_db()
