"""
ui/main_window.py - Main window for the Crop Rotation Assistant GUI.
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QHBoxLayout, QFormLayout, QTextEdit
from PyQt6.QtCore import QSize
from database import DatabaseManager
from logic import CropRotationLogic, SoilRecommendationSystem, TechniqueSuggestion
from classes import Crop, Soil
from data import CROPS, SOILS, TECHNIQUES
from logs_window import LogsWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crop Rotation Assistant")
        self.setFixedSize(QSize(600, 500))
        self.db = DatabaseManager()
        self._init_ui()

    def _init_ui(self):
        # Main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Farmland size
        self.farmland_size_input = QLineEdit()
        self.farmland_size_input.setPlaceholderText("Enter size in acres/hectares")
        form_layout.addRow("Farmland Size:", self.farmland_size_input)

        # Previous crop dropdown
        self.previous_crop_input = QComboBox()
        self.previous_crop_input.addItems([crop.name for crop in CROPS])
        form_layout.addRow("Previous Crop:", self.previous_crop_input)

        # Current crop dropdown
        self.current_crop_input = QComboBox()
        self.current_crop_input.addItems([crop.name for crop in CROPS])
        form_layout.addRow("Current Crop:", self.current_crop_input)

        # Soil type dropdown
        self.soil_type_input = QComboBox()
        self.soil_type_input.addItems([soil.soil_type for soil in SOILS])
        form_layout.addRow("Soil Type:", self.soil_type_input)

        # Submit button
        self.submit_btn = QPushButton("Get Recommendations")
        self.submit_btn.clicked.connect(self.handle_submit)
        form_layout.addRow(self.submit_btn)
        # Add View Logs button
        self.logs_btn = QPushButton("View Logs")
        self.logs_btn.clicked.connect(self.open_logs)
        form_layout.addRow(self.logs_btn)

        # Output area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        # Improved style for readability
        self.output_area.setStyleSheet("""
            background: #ffffff;
            color: #222222;
            font-size: 15px;
            border-radius: 8px;
            padding: 12px;
            border: 1px solid #d0d0d0;
        """)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(QLabel("Recommendations:"))
        main_layout.addWidget(self.output_area)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def handle_submit(self):
        # Validate input
        try:
            farmland_size = float(self.farmland_size_input.text())
            if farmland_size <= 0:
                raise ValueError
        except ValueError:
            self.show_error("Please enter a valid farmland size.")
            return
        previous_crop_name = self.previous_crop_input.currentText()
        current_crop_name = self.current_crop_input.currentText()
        soil_type = self.soil_type_input.currentText()
        # Find crop and soil objects
        prev_crop_obj = next((c for c in CROPS if c.name == previous_crop_name), None)
        curr_crop_obj = next((c for c in CROPS if c.name == current_crop_name), None)
        soil_obj = next((s for s in SOILS if s.soil_type == soil_type), None)
        if not prev_crop_obj or not curr_crop_obj or not soil_obj:
            self.show_error("Invalid crop or soil selection.")
            return
        # Save entry
        self.db.save_user_entry(farmland_size, previous_crop_name, current_crop_name, soil_type)
        # Recommendation logic
        output = ""
        if prev_crop_obj.family == curr_crop_obj.family:
            output += ("<div style='background:#fff3cd;color:#856404;padding:8px;border-radius:6px;border:1px solid #ffeeba;margin-bottom:8px;'>"
                       "<b>Warning:</b> Previous crop and current crop are of the <b>same family</b> (<i>{}</i>). Crop rotation is not recommended!".format(prev_crop_obj.family) + "</div>")
        # Suggest next crops (excluding same family as previous crop)
        next_crops = [crop for crop in CROPS if crop.family != prev_crop_obj.family and soil_type in crop.recommended_soil]
        soil_rec = SoilRecommendationSystem.recommend_soil_management(soil_obj, [prev_crop_obj, curr_crop_obj])
        # Suggest techniques suitable for the soil
        techniques = [t for t in TECHNIQUES if soil_type in t.suitable_soil or "All" in t.suitable_soil]
        # Display output
        output += f"<b>Soil Recommendation:</b> {soil_rec}<br>"
        output += "<b>Suggested Next Crops:</b> " + (", ".join([c.name for c in next_crops]) if next_crops else "No suitable alternatives found.") + "<br>"
        output += "<b>Modern Techniques:</b> " + (", ".join([t.name for t in techniques]) if techniques else "None")
        self.output_area.setHtml(output)

    def open_logs(self):
        self.logs_window = LogsWindow(self)
        self.logs_window.show()
        self.hide()

    def show_error(self, message):
        QMessageBox.critical(self, "Input Error", message)
