from PySide6.QtCore import QObject, QProcess, QTimer, Signal

#Monitors network latency by periodically sending ping requests to a specified host.

class PingMonitor(QObject):

    #Signals used to communicate ping results to the GUI
    ping_updated = Signal(float)
    ping_failed = Signal(str)

    def __init__(self, host: str, interval_ms: int = 2000, parent=None):
        #Initializes the ping monitor.
        super().__init__(parent)

        #Store the target host and the interval between ping requests
        self.host = host
        self.interval_ms = interval_ms

        #Create a process to execute the ping command without blocking the GUI, I believe without this it would freeze
        self.process = QProcess(self)
        self.process.finished.connect(self.handle_ping_result)

        #Create a timer to periodically initiate new ping requests
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_ping)

    def start(self):
        #Start the timer with the configured interval
        self.timer.start(self.interval_ms)
        self.start_ping()

    def stop(self):
        #Stop the timer to prevent further ping requests
        self.timer.stop()
        if self.process.state() != QProcess.NotRunning:
            self.process.kill()

    def start_ping(self):
        #Prevent starting a new ping while another request is still running
        if self.process.state() != QProcess.NotRunning:
            return            
        # Execute the Linux ping command:
        # -c 1: Send a single ICMP echo request
        # -W 1: Wait up to 1 second for a response
        self.process.start("ping", ["-c", "1", "-W", "1", self.host])

    def handle_ping_result(self, *args):

        #Read and decode the standard output and error output of the ping process
        
        output = bytes(self.process.readAllStandardOutput()).decode()
        error_output = bytes(self.process.readAllStandardError()).decode()
        
        #Initialize the variable that will store the measured ping latency
        ping_ms = None

        #Search the command output for the round-trip time
        
        for line in output.splitlines():
            if "time=" in line:
                try:
                    ping_ms = float(line.split("time=")[1].split()[0])
                    break
                except (ValueError, IndexError):
                    pass

        if ping_ms is not None:
            self.ping_updated.emit(ping_ms)
        else:
            error_msg = error_output.strip() or "timeout"
            self.ping_failed.emit(error_msg)
