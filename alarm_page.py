from PySide6.QtWidgets import QWidget, QTableWidgetItem
from ui_alarmpage import Ui_AlarmPage
from alarm import Alarm, AlarmSeverity

class AlarmPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AlarmPage()
        self.ui.setupUi(self)

        self.ui.tableAlarms.setColumnCount(4)
        self.ui.tableAlarms.setHorizontalHeaderLabels(
            ["Time", "Severity", "Code", "Message"]
        )
        self.ui.tableAlarms.horizontalHeader().setStretchLastSection(True)

    def add_alarm(self, alarm: Alarm):
        row = self.ui.tableAlarms.rowCount()
        self.ui.tableAlarms.insertRow(row)

        self.ui.tableAlarms.setItem(row, 0, QTableWidgetItem(alarm.timestamp.strftime("%Y-%m-%d %H:%M:%S")))
        self.ui.tableAlarms.setItem(row, 1, QTableWidgetItem(alarm.severity.name))
        self.ui.tableAlarms.setItem(row, 2, QTableWidgetItem(alarm.code))
        self.ui.tableAlarms.setItem(row, 3, QTableWidgetItem(alarm.message))

    def remove_alarm(self, code: str):
        for row in range(self.ui.tableAlarms.rowCount()):
            item = self.ui.tableAlarms.item(row, 2)
            if item and item.text() == code:
                self.ui.tableAlarms.removeRow(row)
                break
