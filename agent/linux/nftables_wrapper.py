import subprocess
from common.logger import logger

class NFTablesWrapper:
    def __init__(self):
        self.command = "nft"
        self.table_name = "firewall_agent"
        self.chain_name = "input_chain"

    def execute_command(self, args):
        try:
            result = subprocess.run([self.command] + args, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"nftables command failed: {e.stderr.strip()}")
            logger.error(f"Command: {' '.join(e.cmd)}")
            logger.error(f"Return code: {e.returncode}")
            raise

    def initialize(self):
        self.initialize_table_and_chain()
    
    def initialize_table_and_chain(self):
        try:
            # Check if the table already exists
            self.execute_command(["list", "table", "ip", self.table_name])
            logger.info(f"Table {self.table_name} already exists")
        except subprocess.CalledProcessError:
            # Table doesn't exist, so create it
            logger.info(f"Creating table {self.table_name}")
            self.execute_command(["add", "table", "ip", self.table_name])
        
        try:
            # Check if the chain already exists
            self.execute_command(["list", "chain", "ip", self.table_name, self.chain_name])
            logger.info(f"Chain {self.chain_name} already exists")
        except subprocess.CalledProcessError:
            # Chain doesn't exist, so create it
            logger.info(f"Creating chain {self.chain_name}")
            self.execute_command([
                "add", "chain", "ip", self.table_name, self.chain_name, 
                "{ type filter hook input priority 0; policy accept; }"
            ])

    def add_rule(self, rule):
        try:
            args = [
                "add", "rule", "ip", self.table_name, self.chain_name,
                "ip", "saddr", rule[1],  # Source IP
                "ip", "daddr", rule[2],  # Destination IP
                "tcp", "dport", rule[3], # Port
                rule[0]                  # Action (accept, drop, or reject)
            ]
            output = self.execute_command(args)
            logger.info(f"Added rule: {' '.join(args[4:])}")
            return output
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to add rule: {rule}")
            raise

    def delete_rule(self, handle):
        try:
            output = self.execute_command(["delete", "rule", "ip", self.table_name, self.chain_name, "handle", str(handle)])
            logger.info(f"Deleted rule with handle {handle}")
            return output
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to delete rule with handle {handle}")
            raise

    def list_rules(self):
        try:
            output = self.execute_command(["list", "table", "ip", self.table_name])
            logger.info("Listed all rules")
            return output
        except subprocess.CalledProcessError as e:
            logger.error("Failed to list rules")
            raise

    def flush_chain(self):
        try:
            output = self.execute_command(["flush", "chain", "ip", self.table_name, self.chain_name])
            logger.info(f"Flushed chain {self.chain_name}")
            return output
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to flush chain {self.chain_name}")
            raise

    def delete_chain(self):
        try:
            self.execute_command(["delete", "chain", "ip", self.table_name, self.chain_name])
            logger.info(f"Deleted chain {self.chain_name}")
            self.execute_command(["delete", "table", "ip", self.table_name])
            logger.info(f"Deleted table {self.table_name}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to delete chain or table")
            raise

    def add_app_specific_rule(self, app_name, pid, allowed_ports):
        try:
            for port in allowed_ports:
                args = [
                    "add", "rule", "ip", self.table_name, self.chain_name,
                    "meta", "skuid", str(pid),
                    "tcp", "dport", str(port),
                    "accept"
                ]
                self.execute_command(args)
                logger.info(f"Added app-specific rule for {app_name} (PID: {pid}) on port {port}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to add app-specific rule for {app_name} (PID: {pid})")
            raise

    def get_rule_handle(self, rule):
        try:
            output = self.list_rules()
            for line in output.split('\n'):
                if all(component in line for component in rule):
                    handle = line.split('handle')[1].strip()
                    return int(handle)
            logger.warning(f"No handle found for rule: {rule}")
            return None
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get rule handle for: {rule}")
            raise

    def update_rule(self, old_rule, new_rule):
        try:
            handle = self.get_rule_handle(old_rule)
            if handle is not None:
                self.delete_rule(handle)
                self.add_rule(new_rule)
                logger.info(f"Updated rule: {old_rule} -> {new_rule}")
            else:
                logger.warning(f"Rule not found for update: {old_rule}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to update rule: {old_rule} -> {new_rule}")
            raise

    def get_chain_policy(self):
        try:
            output = self.execute_command(["list", "chain", "ip", self.table_name, self.chain_name])
            policy_line = [line for line in output.split('\n') if 'policy' in line][0]
            policy = policy_line.split('policy')[1].strip()
            logger.info(f"Current chain policy: {policy}")
            return policy
        except subprocess.CalledProcessError as e:
            logger.error("Failed to get chain policy")
            raise

    def set_chain_policy(self, policy):
        try:
            self.execute_command([
                "add", "chain", "ip", self.table_name, self.chain_name, 
                f"{{ type filter hook input priority 0; policy {policy}; }}"
            ])
            logger.info(f"Set chain policy to: {policy}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to set chain policy to: {policy}")
            raise