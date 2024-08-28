import subprocess
from common.logger import logger

class IPTablesWrapper:
    def __init__(self):
        self.command = "iptables"

    def execute_command(self, args):
        try:
            result = subprocess.run([self.command] + args, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"iptables command failed: {e.stderr}")
            raise

    def add_rule(self, chain, rule):
        return self.execute_command(["-A", chain] + rule)

    def delete_rule(self, chain, rule):
        return self.execute_command(["-D", chain] + rule)

    def list_rules(self, chain):
        return self.execute_command(["-L", chain, "-n", "-v"])

    def flush_chain(self, chain):
        return self.execute_command(["-F", chain])

    def create_chain(self, chain):
        return self.execute_command(["-N", chain])

    def delete_chain(self, chain):
        return self.execute_command(["-X", chain])

    def add_app_rule(self, app_path, remote_address, remote_port, action):
        chain = "INPUT"
        protocol = "tcp"  # Assuming TCP, adjust as needed
        rule = ["-p", protocol, "-d", remote_address, "--dport", str(remote_port),
                "-m", "owner", "--cmd-owner", app_path, "-j", action.upper()]
        return self.add_rule(chain, rule)

    def remove_app_rule(self, app_path, remote_address, remote_port, action):
        chain = "INPUT"
        protocol = "tcp"  # Assuming TCP, adjust as needed
        rule = ["-p", protocol, "-d", remote_address, "--dport", str(remote_port),
                "-m", "owner", "--cmd-owner", app_path, "-j", action.upper()]
        return self.delete_rule(chain, rule)