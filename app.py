from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import sys
from PyQt6.QtCore import QSize


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        button = QPushButton("Press me!")
        # Set the button to be checkable
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked) # i have call the function that i want when the button is press

        # Set the central widget of the window
        self.setCentralWidget(button)

        # Sizing our window using the qsize 
        self.setFixedSize(QSize(400,300))
    def the_button_was_clicked(self, checked):
        if checked:
            print("Button is checked")
        else:
            print("Button is unchecked")


app = QApplication(sys.argv)
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.


# Start the event loop.
app.exec()