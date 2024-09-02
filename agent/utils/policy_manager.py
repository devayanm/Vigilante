import json
import requests

class PolicyManager:
    def __init__(self, policy_file='policy.json'):
        self.policy_file = policy_file

    def fetch_latest_policy(self):
        """
        Fetch the latest firewall policy from the central web console.
        """
        url = 'http://<web-console-server>/api/get_policy'
        response = requests.get(url)
        if response.status_code == 200:
            policy = response.json()
            self.update_local_policy(policy)
        else:
            print("Failed to fetch policy")

    def update_local_policy(self, policy):
        """
        Update local policy file with the latest firewall rules.
        """
        with open(self.policy_file, 'w') as file:
            json.dump(policy, file)

    def apply_policy(self, firewall_manager):
        """
        Apply the latest firewall policy to the endpoint.
        """
        with open(self.policy_file, 'r') as file:
            policy = json.load(file)
            for rule in policy['rules']:
                firewall_manager.apply_rule(
                    rule['app_name'],
                    rule['remote_ip'],
                    rule['remote_port'],
                    rule['protocol'],
                    rule['action']
                )

if __name__ == "__main__":
    from firewall import FirewallManager
    policy_manager = PolicyManager()
    firewall_manager = FirewallManager()

    policy_manager.fetch_latest_policy()
    policy_manager.apply_policy(firewall_manager)
