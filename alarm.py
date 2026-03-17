from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class AlarmSeverity(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

@dataclass
class Alarm:
    code: str
    message: str
    severity: AlarmSeverity
    timestamp: datetime
    acknowledged: bool = False
