import logging
import os
import platform

def setup_logger(name='firewall_agent'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Determine the log path based on the operating system
    if platform.system().lower() == 'windows':
        log_path = os.path.join(os.environ['APPDATA'], 'FirewallAgent', 'firewall_agent.log')
    else:
        # Default to /var/log but fallback to home directory if permission is denied
        log_path = '/var/log/firewall_agent.log'
        if not os.access('/var/log', os.W_OK):
            log_path = os.path.expanduser('~/firewall_logs/firewall_agent.log')

    # Ensure the directory exists
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # File handler for logging to a file
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Stream handler for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

logger = setup_logger()
