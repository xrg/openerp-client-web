import os
import sys
import thread
import subprocess

# Working Directory
WORK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Update PATH
p = os.environ.get('PATH', '').split(';')

p.insert(0, WORK_DIR)
p.insert(0, WORK_DIR+"\\python25")
p.insert(0, WORK_DIR+"\\python25\\Scripts")

os.environ['PATH'] = ';'.join(p)

# Win32 python extensions modules
import win32serviceutil
import win32service
import win32event
import win32api
import win32con
import win32process
import servicemanager

# The command itself
#EXECUTABLE = ["openerp-web.exe", "--config", "conf\openerp-web.cfg"]
EXECUTABLE = ["python.exe", "python25\Scripts\openerp-web", "--config", "conf\openerp-web.cfg"]

class TinyService(win32serviceutil.ServiceFramework):

    _svc_name_ = "openerp-web"
    _svc_display_name_ = "OpenERP Web"

    _svc_description_ = "OpenERP Web Client"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)

        # Create an event which we will use to wait on.
        # The "service stop" request will set this event.
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

        # a reference to the server's process
        self.proc = None

        # info if the service terminates correctly or if the server crashed
        self.stopping = False


    def SvcStop(self):
        # Before we do anything, tell the SCM we are starting the stop process.
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)

        # stop the running TERP Server: say it's a normal exit
        win32api.TerminateProcess(int(self.proc._handle), 0)
        servicemanager.LogInfoMsg(TinyService._svc_display_name_ + " stopped correctly.")

        # And set my event.
        win32event.SetEvent(self.hWaitStop)

    def StartService(self):

        self.proc = subprocess.Popen(EXECUTABLE, cwd=WORK_DIR,
                                     creationflags=win32process.CREATE_NO_WINDOW)

    def StartControl(self,ws):
        # this listens to the Service Manager's events
        win32event.WaitForSingleObject(ws, win32event.INFINITE)
        self.stopping = True

    def SvcDoRun(self):

        # Start the service itself
        self.StartService()

        # start the loop waiting for the Service Manager's stop signal
        thread.start_new_thread(self.StartControl, (self.hWaitStop,))

        # Log a info message that the server is running
        servicemanager.LogInfoMsg(TinyService._svc_display_name_ + " is up and running.")

        # verification if the server is really running, else quit with an error
        self.proc.wait()

        if not self.stopping:
            sys.exit(TinyService._svc_display_name_ + " is not running, check the logfile for more info.")

if __name__=='__main__':
    # Do with the service whatever option is passed in the command line
    win32serviceutil.HandleCommandLine(TinyService)

