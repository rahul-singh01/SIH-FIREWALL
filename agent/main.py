import sys
import os
import platform
import logging
from logging.handlers import RotatingFileHandler
import argparse

def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'firewall_agent_main.log')
    
    handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    return logger

logger = setup_logging()

# Add Python to PATH if needed (for Windows)
if platform.system().lower() == 'windows':
    python_path = r"C:\Users\rahul\AppData\Local\Programs\Python\Python312"
    scripts_path = os.path.join(python_path, 'Scripts')
    os.environ['PATH'] = f"{python_path};{scripts_path};{os.environ['PATH']}"


def run_windows_agent(command):
    try:
        import win32serviceutil
        from windows.win_service import FirewallAgentService
        
        if command == 'install':
            sys.argv = [sys.argv[0], 'install']
            win32serviceutil.HandleCommandLine(FirewallAgentService)
            logger.info("Windows Firewall Agent service installed")
        elif command == 'start':
            win32serviceutil.StartService(FirewallAgentService._svc_name_)
            logger.info("Windows Firewall Agent service started")
        elif command == 'stop':
            win32serviceutil.StopService(FirewallAgentService._svc_name_)
            logger.info("Windows Firewall Agent service stopped")
        elif command == 'restart':
            win32serviceutil.RestartService(FirewallAgentService._svc_name_)
            logger.info("Windows Firewall Agent service restarted")
        elif command == 'remove':
            sys.argv = [sys.argv[0], 'remove']
            win32serviceutil.HandleCommandLine(FirewallAgentService)
            logger.info("Windows Firewall Agent service removed")
        elif command == 'run':
            from windows.firewall_agent import WindowsFirewallAgent
            agent = WindowsFirewallAgent()
            agent.run()
        else:
            logger.error(f"Unknown command: {command}")
    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        logger.error("Make sure pywin32 is installed: pip install pywin32")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error executing command {command}: {e}")
        sys.exit(1)

def run_linux_agent(command):
    try:
        from linux.linux_daemon import FirewallAgentDaemon
        daemon = FirewallAgentDaemon('/tmp/firewall_agent.pid')
        
        if command == 'start':
            daemon.start()
        elif command == 'stop':
            daemon.stop()
        elif command == 'restart':
            daemon.restart()
        else:
            logger.error(f"Unknown command: {command}")
            sys.exit(1)
    except ImportError as e:
        logger.error(f"Failed to import FirewallAgentDaemon: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error executing command {command}: {e}")
        sys.exit(1)

def run_as_service():
    try:
        import servicemanager
        import win32serviceutil
        from windows.win_service import FirewallAgentService

        if len(sys.argv) == 1:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(FirewallAgentService)
            servicemanager.StartServiceCtrlDispatcher()
        else:
            win32serviceutil.HandleCommandLine(FirewallAgentService)
    except ImportError as e:
        logger.error(f"Failed to import required modules for Windows service: {e}")
        logger.error("Make sure pywin32 is installed: pip install pywin32")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Firewall Agent Control Script")
    parser.add_argument('command', choices=['install', 'start', 'stop', 'restart', 'remove', 'run'], 
                        help="Command to execute (install, start, stop, restart, remove, or run)")
    parser.add_argument('--service', action='store_true', help="Run as a Windows service")
    args = parser.parse_args()

    os_type = platform.system().lower()
    logger.info(f"Detected OS: {os_type}")

    if os_type == 'windows':
        if args.service:
            run_as_service()
        else:
            run_windows_agent(args.command)
    elif os_type == 'linux':
        run_linux_agent(args.command)
    else:
        logger.error(f"Unsupported operating system: {os_type}")
        sys.exit(1)

if __name__ == "__main__":
    logger.info("Script started")
    main()