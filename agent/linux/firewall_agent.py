import time
from common.logger import logger
from common.config import config
from .iptables_wrapper import IPTablesWrapper
from .process_monitor import ProcessMonitor
from .log_collector import LogCollector

class LinuxFirewallAgent:
    def __init__(self):
        self.iptables = IPTablesWrapper()
        self.process_monitor = ProcessMonitor()
        self.log_collector = LogCollector()

    def initialize(self):
        # Create a custom chain for our rules
        self.iptables.create_chain("FIREWALL_AGENT")
        self.iptables.add_rule("INPUT", ["-j", "FIREWALL_AGENT"])

    def run(self):
        logger.info("Starting Linux Firewall Agent")
        self.initialize()
        
        try:
            while True:
                self.check_new_processes()
                self.apply_policies()
                self.collect_and_send_logs()
                time.sleep(config.get('check_interval', 60))
        except KeyboardInterrupt:
            logger.info("Stopping Linux Firewall Agent")
        finally:
            self.cleanup()

    def check_new_processes(self):
        for process in self.process_monitor.monitor():
            self.handle_new_process(process)

    def handle_new_process(self, process):
        # Implementation to handle new processes
        # This could involve checking against policies and applying rules
        logger.info(f"Handling new process: {process['name']}")

    def apply_policies(self):
        # Fetch and apply policies from the central server
        # This is a placeholder and would need to be implemented
        logger.info("Applying policies")

    def collect_and_send_logs(self):
        logs = self.log_collector.collect_logs()
        self.log_collector.send_logs(logs)

    def cleanup(self):
        # Remove our custom chain
        self.iptables.delete_rule("INPUT", ["-j", "FIREWALL_AGENT"])
        self.iptables.flush_chain("FIREWALL_AGENT")
        self.iptables.delete_chain("FIREWALL_AGENT")