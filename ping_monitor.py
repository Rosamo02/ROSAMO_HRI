from PySide6.QtCore import QObject, QProcess, QTimer, Signal


class PingMonitor(QObject):
    ping_updated = Signal(float)
    ping_failed = Signal(str)

    def __init__(self, host: str, interval_ms: int = 2000, parent=None):
        super().__init__(parent)

        self.host = host
        self.interval_ms = interval_ms

        self.process = QProcess(self)
        self.process.finished.connect(self.handle_ping_result)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_ping)

    def start(self):
        self.timer.start(self.interval_ms)
        self.start_ping()

    def stop(self):
        self.timer.stop()
        if self.process.state() != QProcess.NotRunning:
            self.process.kill()

    def start_ping(self):
        if self.process.state() != QProcess.NotRunning:
            return

        self.process.start("ping", ["-c", "1", "-W", "1", self.host])

    def handle_ping_result(self, *args):
        output = bytes(self.process.readAllStandardOutput()).decode()
        error_output = bytes(self.process.readAllStandardError()).decode()

        ping_ms = None
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
