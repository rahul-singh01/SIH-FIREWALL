import psutil
from common.logger import logger

class ProcessMonitor:
    def __init__(self):
        self.previous_processes = set()

    def get_new_processes(self):
        current_processes = set(psutil.process_iter(['pid', 'name', 'exe']))
        new_processes = current_processes - self.previous_processes
        self.previous_processes = current_processes
        return new_processes

    def monitor(self):
        new_processes = self.get_new_processes()
        for process in new_processes:
            try:
                logger.info(f"New process detected: PID={process.pid}, Name={process.name()}, Exe={process.exe()}")
                yield {
                    'pid': process.pid,
                    'name': process.name(),
                    'exe': process.exe()
                }
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass