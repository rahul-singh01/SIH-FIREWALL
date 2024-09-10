from common.logger import logger
from common.config import config
from common.database import Database
from .nftables_wrapper import NFTablesWrapper
from .process_monitor import ProcessMonitor
import time
import threading
import signal
import sys
import hashlib

class LinuxFirewallAgent:
    def __init__(self):
        self.nftables = NFTablesWrapper()
        self.process_monitor = ProcessMonitor()
        self.db = Database(config)
        self.policies = None
        self.applications = None
        self.running = False
        self.lock = threading.Lock()
        self.applied_policies_hash = None
        self.last_policy_check = 0

    def initialize(self):
        logger.info("Initializing NFTables for Firewall Agent")
        try:
            self.nftables.initialize()
            self.fetch_policies_and_applications()
            self.set_default_chain_policy()
        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            self.alert("high", f"Firewall initialization failed: {str(e)}")
            raise

    def set_default_chain_policy(self):
        default_policy = config.DEFAULT_CHAIN_POLICY
        try:
            current_policy = self.nftables.get_chain_policy()
            if current_policy != default_policy:
                self.nftables.set_chain_policy(default_policy)
                logger.info(f"Set default chain policy to: {default_policy}")
        except Exception as e:
            logger.error(f"Failed to set default chain policy: {str(e)}")
            self.alert("medium", f"Failed to set default chain policy: {str(e)}")

    def fetch_policies_and_applications(self):
        try:
            self.policies = self.db.get_policies()
            self.applications = self.db.get_applications()
            if self.policies and self.applications:
                logger.info("Successfully fetched policies and applications")
            else:
                logger.warning("Failed to fetch policies or applications")
                self.alert("medium", "Failed to fetch policies or applications")
        except Exception as e:
            logger.error(f"Error fetching policies and applications: {str(e)}")
            self.alert("high", f"Database error: {str(e)}")

    def fetch_and_apply_policies(self):
        current_time = time.time()
        if current_time - self.last_policy_check < config.POLICY_CHECK_INTERVAL:
            return

        try:
            new_policies = self.db.get_policies()
            new_policies_hash = self.hash_policies(new_policies)

            if new_policies_hash != self.applied_policies_hash:
                logger.info("Policy changes detected. Applying new policies.")
                self.apply_policies(new_policies)
                self.applied_policies_hash = new_policies_hash
                self.policies = new_policies
            else:
                logger.debug("No policy changes detected.")

            self.last_policy_check = current_time
        except Exception as e:
            logger.error(f"Error fetching or applying policies: {str(e)}")
            self.alert("high", f"Policy update error: {str(e)}")

    def hash_policies(self, policies):
        policy_str = str(sorted(policies, key=lambda x: x['id']))
        return hashlib.md5(policy_str.encode()).hexdigest()

    def apply_policies(self, new_policies):
        try:
            with self.lock:
                current_rules = self.nftables.list_rules()
                for policy in new_policies:
                    self.apply_single_policy(policy, current_rules)
                
                # Remove rules that are no longer in the policies
                self.remove_obsolete_rules(new_policies, current_rules)

            self.log("high", "Successfully applied new policies")
            logger.info("Successfully applied all new policies")
        except Exception as e:
            logger.error(f"Error applying policies: {str(e)}")
            self.alert("high", f"Failed to apply new policies: {str(e)}")

    def apply_single_policy(self, policy, current_rules):
        try:
            action = policy['action'].lower()
            if action == "allow":
                action = "accept"
            elif action not in ["accept", "drop", "reject"]:
                logger.warning(f"Invalid action in policy: {policy['action']}")
                return

            rule = [
                action,
                policy['source_ip'],
                policy['destination_ip'],
                str(policy['port'])
            ]
            
            rule_str = ' '.join(rule)
            if rule_str in current_rules:
                logger.debug(f"Rule already exists: {rule_str}")
            else:
                self.nftables.add_rule(rule)
                logger.info(f"Applied new policy: {rule}")
        except KeyError as e:
            logger.error(f"Missing key in policy: {str(e)}")
        except Exception as e:
            logger.error(f"Error applying single policy: {str(e)}")

    def remove_obsolete_rules(self, new_policies, current_rules):
        new_rule_set = set(' '.join([
            policy['action'].lower() if policy['action'].lower() != 'allow' else 'accept',
            policy['source_ip'],
            policy['destination_ip'],
            str(policy['port'])
        ]) for policy in new_policies)

        for rule in current_rules.split('\n'):
            if rule and rule not in new_rule_set:
                try:
                    handle = self.nftables.get_rule_handle(rule.split())
                    if handle:
                        self.nftables.delete_rule(handle)
                        logger.info(f"Removed obsolete rule: {rule}")
                except Exception as e:
                    logger.error(f"Error removing obsolete rule: {str(e)}")

    def run(self):
        logger.info("Starting Linux Firewall Agent")
        self.initialize()
        self.running = True
        
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        
        try:
            self.log("low", "Firewall agent running normally")
            while self.running:
                self.check_new_processes()
                self.fetch_and_apply_policies()
                time.sleep(config.CHECK_INTERVAL)
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {str(e)}")
            self.alert("high", f"Firewall agent encountered an error: {str(e)}")
        finally:
            self.cleanup()

    def signal_handler(self, signum, frame):
        logger.info(f"Received signal {signum}. Stopping Linux Firewall Agent")
        self.running = False

    def check_new_processes(self):
        try:
            processes = self.process_monitor.monitor()
            for process in processes:
                logger.debug(f"Process data: {process}")
                self.handle_new_process(process)
        except Exception as e:
            logger.error(f"Error monitoring processes: {str(e)}")
            self.alert("medium", f"Process monitoring error: {str(e)}")

    def handle_new_process(self, process):
        process_name = process.get('name')
        process_pid = process.get('pid')
        if not process_name or not process_pid:
            logger.warning(f"Invalid process data: {process}")
            return

        logger.info(f"New process detected: {process_name} (PID: {process_pid})")
        with self.lock:
            if self.applications:
                app = next((a for a in self.applications if a.name == process_name), None)
                if app:
                    self.apply_app_specific_rules(process, app)
                else:
                    logger.info(f"No specific rules for application: {process_name}")
            else:
                logger.warning("No application data available")

    def apply_app_specific_rules(self, process, app):
        try:
            logger.info(f"Applying rules for application: {app.name}")
            self.nftables.add_app_specific_rule(app.name, process['pid'], app.allowed_ports)
            self.log("info", f"Applied rules for application: {app.name}")
        except Exception as e:
            logger.error(f"Error applying rules for {app.name}: {str(e)}")
            self.alert("medium", f"Failed to apply rules for {app.name}: {str(e)}")

    def log(self, level, message):
        try:
            # timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.db.add_log(level, message)
        except Exception as e:
            logger.error(f"Failed to add log: {str(e)}")

    def alert(self, level, message):
        try:
            self.db.add_alert(level, message)
            logger.warning(f"Alert ({level}): {message}")
        except Exception as e:
            logger.error(f"Failed to add alert: {str(e)}")

    def cleanup(self):
        logger.info("Cleaning up NFTables rules")
        try:
            self.nftables.flush_chain()
            self.nftables.delete_chain()
        except Exception as e:
            logger.error(f"Error cleaning up NFTables: {str(e)}")
        finally:
            self.db.close()

# def main():
#     agent = LinuxFirewallAgent()
#     try:
#         agent.run()
#     except Exception as e:
#         logger.critical(f"Critical error in Firewall Agent: {str(e)}")
#         sys.exit(1)

# if __name__ == "__main__":
#     main()