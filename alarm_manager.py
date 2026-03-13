from PySide6.QtCore import QObject, Signal
from datetime import datetime
from alarm import Alarm, AlarmSeverity

class AlarmManager(QObject):
    alarmRaised = Signal(Alarm)
    alarmCleared = Signal(str)
    unacknowledgedChanged = Signal(bool)

    def __init__(self):
        super().__init__()
        self._active_alarms = {}
        self._unacknowledged = False

    def raise_alarm(self, code, message, severity):
        if code in self._active_alarms:
            return

        alarm = Alarm(code, message, severity, datetime.now())
        self._active_alarms[code] = alarm

        self._unacknowledged = True
        self.unacknowledgedChanged.emit(True)

        self.alarmRaised.emit(alarm)

    def acknowledge(self):
        self._unacknowledged = False
        self.unacknowledgedChanged.emit(False)

