import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import time
import logging
from logging.handlers import RotatingFileHandler

class FirewallAgentService(win32serviceutil.ServiceFramework):
    _svc_name_ = "FirewallAgentService"
    _svc_display_name_ = "Firewall Agent Service"
    _svc_description_ = "Firewall Agent Service for managing firewall rules"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    @classmethod
    def get_class_string(cls):
        # Use pythonw.exe instead of python.exe
        return f'"{sys.executable}w" "{os.path.abspath(sys.argv[0])}" {cls._svc_name_}'

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        while True:
            if win32event.WaitForSingleObject(self.hWaitStop, 5000) == win32event.WAIT_OBJECT_0:
                break

        try:
            from .firewall_agent import WindowsFirewallAgent
            agent = WindowsFirewallAgent()
            self.logger.info("Running WindowsFirewallAgent...")
            
            while self.is_alive:
                agent.run()
                time.sleep(1)  # Adjust sleep time as needed
        except Exception as e:
            self.logger.error(f"Error in FirewallAgentService: {str(e)}")
            self.logger.exception("Full traceback:")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(FirewallAgentService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(FirewallAgentService)