import sys
import os
import platform

import logging
logging.basicConfig(filename='/coding/django/SIH_FIREWALL/agent/logs/firewall_agent_main.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_windows_agent():
    from windows.firewall_agent import WindowsFirewallAgent
    agent = WindowsFirewallAgent()
    agent.run()

def run_linux_agent():
    from linux.linux_daemon import FirewallAgentDaemon
    daemon = FirewallAgentDaemon('/tmp/firewall_agent.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)

def run_as_service():
    import servicemanager
    import win32serviceutil
    import win32service
    import win32event
    from windows.win_service import FirewallAgentService

    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(FirewallAgentService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(FirewallAgentService)

def main():
    os_type = platform.system().lower()
    
    # #  os_type = platform.system().lower()
    logger.info(f"Detected OS: {os_type}")
 
    if os_type == 'windows':
        if len(sys.argv) > 1 and sys.argv[1] == '--service':
            run_as_service()
        else:
            run_windows_agent()
    elif os_type == 'linux':
        run_linux_agent()
    else:
        print(f"Unsupported operating system: {os_type}")
        sys.exit(1)

   
        
if __name__ == "__main__":
    logger.info("Script started")
    main()