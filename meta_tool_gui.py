from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QComboBox, QGroupBox,
    QRadioButton, QMessageBox
)
from PyQt6.QtCore import Qt
import sys
import os
from meta_tool.conflict_resolver import ConflictResolver
import logging

logger = logging.getLogger('MetaTool')

class MetaToolGUI(QMainWindow):
    def __init__(self):
        try:
            logger.info("Initializing MetaToolGUI")
            super().__init__()
            self.carcols_path = ""
            self.variations_path = ""
            self.resolver = None
            logger.info("Calling init_ui")
            self.init_ui()
            logger.info("GUI initialization complete")
        except Exception as e:
            logger.exception("Error in MetaToolGUI initialization")
            raise

    def init_ui(self):
        try:
            logger.info("Setting up UI components")
            self.setWindowTitle('FiveM Meta Tool')
            self.setGeometry(100, 100, 800, 600)

            # Create central widget and layout
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)

            # File Selection
            file_group = QGroupBox("Meta Files")
            file_layout = QVBoxLayout()

            # Carcols selection
            carcols_layout = QHBoxLayout()
            self.carcols_label = QLabel("No carcols.meta selected")
            carcols_btn = QPushButton("Select Carcols.meta")
            carcols_btn.clicked.connect(self.select_carcols)
            carcols_layout.addWidget(self.carcols_label)
            carcols_layout.addWidget(carcols_btn)
            file_layout.addLayout(carcols_layout)

            # Variations selection
            variations_layout = QHBoxLayout()
            self.variations_label = QLabel("No carvariations.meta selected")
            variations_btn = QPushButton("Select Carvariations.meta")
            variations_btn.clicked.connect(self.select_variations)
            variations_layout.addWidget(self.variations_label)
            variations_layout.addWidget(variations_btn)
            file_layout.addLayout(variations_layout)

            file_group.setLayout(file_layout)
            layout.addWidget(file_group)

            # Operation Selection
            operation_group = QGroupBox("Operation")
            operation_layout = QVBoxLayout()
            self.carcols_radio = QRadioButton("Carcols Conflict Resolution")
            self.modkit_radio = QRadioButton("Modkit ID Resolution")
            self.carcols_radio.setChecked(True)
            operation_layout.addWidget(self.carcols_radio)
            operation_layout.addWidget(self.modkit_radio)
            operation_group.setLayout(operation_layout)
            layout.addWidget(operation_group)

            # Vehicle Selection
            vehicle_group = QGroupBox("Vehicle")
            vehicle_layout = QVBoxLayout()
            self.vehicle_combo = QComboBox()
            self.vehicle_combo.addItem("All Vehicles")
            vehicle_layout.addWidget(self.vehicle_combo)
            vehicle_group.setLayout(vehicle_layout)
            layout.addWidget(vehicle_group)

            # Process Button
            self.process_btn = QPushButton("Process")
            self.process_btn.clicked.connect(self.process_files)
            self.process_btn.setEnabled(False)
            layout.addWidget(self.process_btn)
            logger.info("UI setup complete")
        except Exception as e:
            logger.exception("Error in MetaToolGUI initialization")
            raise

    def select_carcols(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Carcols.meta", "", "Meta Files (*.meta);;All Files (*)"
        )
        if file_path:
            self.carcols_path = file_path
            self.carcols_label.setText(os.path.basename(file_path))
            self.update_process_button()
            self.update_vehicle_list()

    def select_variations(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Carvariations.meta", "", "Meta Files (*.meta);;All Files (*)"
        )
        if file_path:
            self.variations_path = file_path
            self.variations_label.setText(os.path.basename(file_path))
            self.update_process_button()
            self.update_vehicle_list()

    def update_process_button(self):
        self.process_btn.setEnabled(bool(self.carcols_path and self.variations_path))

    def update_vehicle_list(self):
        if self.carcols_path and self.variations_path:
            try:
                self.resolver = ConflictResolver(self.carcols_path, self.variations_path)
                self.vehicle_combo.clear()
                self.vehicle_combo.addItem("All Vehicles")
                # Add vehicles from meta files
                vehicles = self.resolver.get_vehicle_list()
                self.vehicle_combo.addItems(vehicles)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error loading files: {str(e)}")

    def process_files(self):
        if not self.resolver:
            return

        try:
            selected_vehicle = None
            if self.vehicle_combo.currentText() != "All Vehicles":
                selected_vehicle = self.vehicle_combo.currentText()

            if self.carcols_radio.isChecked():
                self.resolver.resolve_carcols_conflicts(selected_vehicle)
                operation = "Carcols"
            else:
                self.resolver.resolve_modkit_conflicts(selected_vehicle)
                operation = "Modkit"

            msg = f"{operation} conflicts resolved successfully!"
            if selected_vehicle:
                msg += f" for vehicle: {selected_vehicle}"
            QMessageBox.information(self, "Success", msg)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error processing files: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = MetaToolGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()