import time
from traffic_monitor import monitor_traffic
from firewall import FirewallManager
from logger import TrafficLogger
from utils.policy_manager import PolicyManager

class FirewallAgent:
    def __init__(self):
        self.firewall_manager = FirewallManager()
        self.logger = TrafficLogger()
        self.policy_manager = PolicyManager()

    def run(self):
        """
        Main loop to monitor traffic, apply policies, and log data.
        """
        self.policy_manager.fetch_latest_policy()
        self.policy_manager.apply_policy(self.firewall_manager)

        while True:
            traffic_data = monitor_traffic()
            self.logger.log_traffic(traffic_data)
            self.logger.send_logs_to_server(traffic_data)

            time.sleep(5)  # Adjust the interval based on requirements

if __name__ == "__main__":
    agent = FirewallAgent()
    agent.run()
