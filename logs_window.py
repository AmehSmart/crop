"""
ui/logs_window.py - Window to display all saved crop recommendations/logs.
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel
from PyQt6.QtCore import QSize
from database import DatabaseManager

class LogsWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Recommendation Logs")
        self.setFixedSize(QSize(700, 400))
        self.db = DatabaseManager()
        self.main_window = main_window
        self._init_ui()

    def _init_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("<b>All Recommendation Logs</b>")
        layout.addWidget(label)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Farmland Size", "Previous Crop", "Current Crop", "Soil Type"])
        self.load_logs()
        layout.addWidget(self.table)
        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.go_back)
        layout.addWidget(self.back_btn)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def load_logs(self):
        logs = self.db.get_user_entries()
        self.table.setRowCount(len(logs))
        for row, entry in enumerate(logs):
            # entry: (id, farmland_size, previous_crop, current_crop, soil_type)
            self.table.setItem(row, 0, QTableWidgetItem(str(entry[1])))
            self.table.setItem(row, 1, QTableWidgetItem(entry[2]))
            self.table.setItem(row, 2, QTableWidgetItem(entry[3]))
            self.table.setItem(row, 3, QTableWidgetItem(entry[4]))
        self.table.resizeColumnsToContents()

    def go_back(self):
        self.main_window.show()
        self.close()
