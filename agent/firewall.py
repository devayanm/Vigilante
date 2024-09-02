import subprocess
import platform

class FirewallManager:
    def __init__(self):
        self.os_type = platform.system()

    def apply_rule(self, app_name, remote_ip, remote_port, protocol, action):
        """
        Apply firewall rule based on application, IP, port, and protocol.
        Action: Allow or Deny traffic
        """
        if self.os_type == "Linux":
            self._apply_rule_linux(app_name, remote_ip, remote_port, protocol, action)
        elif self.os_type == "Windows":
            self._apply_rule_windows(app_name, remote_ip, remote_port, protocol, action)

    def _apply_rule_linux(self, app_name, remote_ip, remote_port, protocol, action):
        """
        Apply firewall rule on Linux using iptables.
        """
        action_flag = "-A" if action == "Allow" else "-D"
        command = [
            "iptables",
            action_flag,
            "OUTPUT",
            "-p", protocol.lower(),
            "--dport", str(remote_port),
            "-d", remote_ip,
            "-m", "owner", "--cmd-owner", app_name,
            "-j", "ACCEPT" if action == "Allow" else "DROP"
        ]
        subprocess.run(command, check=True)

    def _apply_rule_windows(self, app_name, remote_ip, remote_port, protocol, action):
        """
        Apply firewall rule on Windows using netsh.
        """
        action_flag = "allow" if action == "Allow" else "block"
        command = [
            "netsh", "advfirewall", "firewall", "add", "rule",
            f"name={app_name} rule",
            f"dir=out action={action_flag}",
            f"remoteip={remote_ip} remoteport={remote_port}",
            f"protocol={protocol.lower()}"
        ]
        subprocess.run(command, check=True)

    def remove_rule(self, app_name, remote_ip, remote_port, protocol):
        """
        Remove a previously applied firewall rule.
        """
        self.apply_rule(app_name, remote_ip, remote_port, protocol, "Deny")

if __name__ == "__main__":
    firewall = FirewallManager()
    firewall.apply_rule("firefox", "192.168.1.1", 80, "TCP", "Allow")
