import win32serviceutil
import win32service
import win32event
import servicemanager
import socket

from api_abpylogix import app  # Import your Flask app instance

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ab_pylogix_api.py"
    _svc_display_name_ = "ABPLCService"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.app = app

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.app.run(host='127.0.0.1', port=5000)  # Modify host and port as needed

if __name__ == '__main__':
    servicemanager.Initialize()
    servicemanager.PrepareToHostSingle(MyService)
    servicemanager.StartServiceCtrlDispatcher()
