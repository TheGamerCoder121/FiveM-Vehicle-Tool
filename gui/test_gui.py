from PyQt6.QtWidgets import QApplication, QLabel
import sys

app = QApplication(sys.argv)
label = QLabel("PyQt6 Test")
label.show()
sys.exit(app.exec())