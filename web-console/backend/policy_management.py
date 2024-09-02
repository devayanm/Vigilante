import json
from models.policy_model import PolicyModel

class PolicyManager:
    def __init__(self):
        self.policy_model = PolicyModel()

    def get_latest_policy(self):
        """
        Retrieve the latest firewall policy from the database.
        """
        policy = self.policy_model.get_policy()
        if not policy:
            policy = {
                "rules": []
            }
        return policy

    def update_policy(self, new_policy):
        """
        Update the firewall policy in the database.
        """
        policy_json = json.dumps(new_policy)
        self.policy_model.update_policy(policy_json)
