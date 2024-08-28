import psutil
import time
from common.logger import logger

class LogCollector:
    def __init__(self):
        self.last_collection_time = time.time()

    def collect_logs(self):
        current_time = time.time()
        logs = []
        for conn in psutil.net_connections():
            if conn.status == psutil.CONN_ESTABLISHED:
                try:
                    process = psutil.Process(conn.pid)
                    logs.append({
                        'timestamp': current_time,
                        'pid': conn.pid,
                        'process_name': process.name(),
                        'local_address': conn.laddr.ip,
                        'local_port': conn.laddr.port,
                        'remote_address': conn.raddr.ip,
                        'remote_port': conn.raddr.port,
                        'status': conn.status
                    })
                except psutil.NoSuchProcess:
                    pass
        self.last_collection_time = current_time
        return logs

    def send_logs(self, logs):
        # Implementation to send logs to the central server
        # This is a placeholder and would need to be implemented
        logger.info(f"Sending {len(logs)} log entries to central server")