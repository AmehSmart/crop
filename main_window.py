from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox, QFormLayout, QTextEdit, QGridLayout,
    QScrollArea, QFrame, QSplitter
)
from PyQt6.QtCore import QSize, QTimer, QPropertyAnimation, QEasingCurve, QRect, pyqtProperty, Qt
from PyQt6.QtGui import QPalette, QColor, QFont
import sys

from database import DatabaseManager
from logic import CropRotationLogic, SoilRecommendationSystem, TechniqueSuggestion
from data import CROPS, SOILS, TECHNIQUES
from logs_window import LogsWindow


class AnimatedWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._opacity = 1.0
        self.animation = QPropertyAnimation(self, b"opacity")
        self.animation.setDuration(2000)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
    def get_opacity(self):
        return self._opacity
    
    def set_opacity(self, value):
        self._opacity = value
        self.update()
    
    opacity = pyqtProperty(float, get_opacity, set_opacity)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Crop Rotation Assistant")
        self.setMinimumSize(QSize(1200, 700))  # Wider minimum size for grid layout
        self.resize(QSize(1400, 800))  # Larger default size
        self.db = DatabaseManager()
        self.rotation_logic = CropRotationLogic()
        self._init_ui()
        self._apply_theme()
        self._setup_animations()

    def _setup_animations(self):
        # Subtle fade-in animation on startup
        self.fade_timer = QTimer()
        self.fade_timer.timeout.connect(self._animate_background)
        self.fade_timer.start(3000)  # Change every 3 seconds
        
    def _animate_background(self):
        # This will trigger a subtle color shift in the background
        self.update()

    def _apply_theme(self):
        self.setStyleSheet("""
            QMainWindow { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #e8f4e8, stop:0.25 #f0f8f0, 
                    stop:0.5 #f5faf5, stop:0.75 #f8fcf8, stop:1 #fafefa);
            }
            
            QWidget {
                background: transparent;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QLabel { 
                color: #2d4a2d; 
                font-size: 14px; 
                font-weight: 600;
                background: transparent;
            }
            
            QLineEdit {
                background-color: #ffffff;
                color: #333333;
                border: 2px solid #90c695;
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 14px;
                font-weight: 500;
                selection-background-color: #c8e6c9;
            }
            
            QLineEdit:focus {
                border: 2px solid #4caf50;
                background-color: #f8fff8;
                box-shadow: 0px 0px 8px rgba(76, 175, 80, 0.3);
            }
            
            QLineEdit:hover {
                border: 2px solid #66bb6a;
                background-color: #fcfffc;
            }
            
            QComboBox {
                background-color: #ffffff;
                color: #333333;
                border: 2px solid #90c695;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                font-weight: 500;
                min-height: 20px;
            }
            
            QComboBox:focus {
                border: 2px solid #4caf50;
                background-color: #f8fff8;
            }
            
            QComboBox:hover {
                border: 2px solid #66bb6a;
                background-color: #fcfffc;
            }
            
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #90c695;
                background: #e8f4e8;
                border-radius: 0px 6px 6px 0px;
            }
            
            QComboBox::down-arrow {
                image: none;
                width: 0;
                height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid #4caf50;
            }
            
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                border: 2px solid #90c695;
                border-radius: 8px;
                selection-background-color: #c8e6c9;
                color: #333333;
                padding: 5px;
            }
            
            QTextEdit {
                background-color: #ffffff;
                color: #333333;
                border: 2px solid #90c695;
                border-radius: 10px;
                padding: 15px;
                font-size: 14px;
                line-height: 1.4;
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #66bb6a, stop:0.5 #4caf50, stop:1 #43a047);
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 18px;
                border-radius: 10px;
                border: none;
                min-width: 120px;
            }
            
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5cb85c, stop:0.5 #449d44, stop:1 #398439);
                transform: translateY(-2px);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #449d44, stop:1 #357a35);
            }
            
            QPushButton:disabled { 
                background: #cccccc;
                color: #888888;
            }
            
            QFrame {
                background: transparent;
            }
            
            QSplitter::handle {
                background: #90c695;
                border: 1px solid #4caf50;
                border-radius: 3px;
            }
            
            QSplitter::handle:horizontal {
                width: 6px;
            }
            
            QSplitter::handle:vertical {
                height: 6px;
            }
        """)

    def _init_ui(self):
        main_widget = QWidget()
        
        # Create main horizontal layout (grid system)
        main_layout = QHBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # LEFT PANEL - Input Form
        left_panel = QFrame()
        left_panel.setFrameStyle(QFrame.Shape.StyledPanel)
        left_panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.98), 
                    stop:0.5 rgba(248, 255, 248, 0.95), 
                    stop:1 rgba(245, 250, 245, 0.98));
                border-radius: 15px;
                border: 2px solid rgba(144, 198, 149, 0.6);
                padding: 10px;
            }
        """)
        left_layout = QVBoxLayout()
        left_layout.setSpacing(20)
        left_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title for left panel
        title_label = QLabel("🌾 Smart Crop Rotation Assistant")
        title_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2d4a2d;
            text-align: center;
            padding: 15px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(255,255,255,0.8), 
                stop:0.5 rgba(248,255,248,0.9), 
                stop:1 rgba(255,255,255,0.8));
            border-radius: 12px;
            border: 1px solid rgba(144, 198, 149, 0.5);
            margin-bottom: 10px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Form section
        form_widget = QWidget()
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(0, 0, 0, 0)

        # Farmland size
        self.farmland_size_input = QLineEdit()
        self.farmland_size_input.setPlaceholderText("Enter size (e.g., 2.5 acres)")
        form_layout.addRow("🌾 Farmland Size:", self.farmland_size_input)

        # Previous crop
        self.previous_crop_input = QComboBox()
        self.previous_crop_input.addItems([c.name for c in CROPS])
        form_layout.addRow("🌱 Previous Crop:", self.previous_crop_input)

        # Current crop
        self.current_crop_input = QComboBox()
        self.current_crop_input.addItems([c.name for c in CROPS])
        form_layout.addRow("🌿 Current Crop:", self.current_crop_input)

        # Soil type
        self.soil_type_input = QComboBox()
        self.soil_type_input.addItems([s.soil_type for s in SOILS])
        form_layout.addRow("🏔️ Soil Type:", self.soil_type_input)

        form_widget.setLayout(form_layout)
        
        # Buttons section
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.submit_btn = QPushButton("🔍 Get Recommendations")
        self.submit_btn.clicked.connect(self.handle_submit)
        self.submit_btn.setStyleSheet("""
            QPushButton {
                padding: 15px 20px;
                font-size: 16px;
                min-height: 20px;
            }
        """)
        
        self.logs_btn = QPushButton("📋 View Logs")
        self.logs_btn.clicked.connect(self.open_logs)
        
        buttons_layout.addWidget(self.submit_btn)
        buttons_layout.addWidget(self.logs_btn)

        # Alternative picker (hidden until needed)
        self.alternatives_widget = QWidget()
        alternatives_layout = QVBoxLayout()
        alternatives_layout.setContentsMargins(0, 10, 0, 0)
        
        self.alternative_label = QLabel("💡 Suggested Alternatives:")
        self.alternative_label.setStyleSheet("font-weight: bold; color: #e65100;")
        self.alternative_combo = QComboBox()
        self.apply_alt_btn = QPushButton("✅ Apply Alternative")
        self.apply_alt_btn.clicked.connect(self.apply_alternative)
        
        alternatives_layout.addWidget(self.alternative_label)
        alternatives_layout.addWidget(self.alternative_combo)
        alternatives_layout.addWidget(self.apply_alt_btn)
        
        self.alternatives_widget.setLayout(alternatives_layout)
        self.alternatives_widget.setVisible(False)

        # Assemble left panel
        left_layout.addWidget(title_label)
        left_layout.addWidget(form_widget)
        left_layout.addLayout(buttons_layout)
        left_layout.addWidget(self.alternatives_widget)
        left_layout.addStretch()  # Push everything to top
        
        left_panel.setLayout(left_layout)
        
        # RIGHT PANEL - Recommendations
        right_panel = QFrame()
        right_panel.setFrameStyle(QFrame.Shape.StyledPanel)
        right_panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.98), 
                    stop:0.5 rgba(248, 255, 248, 0.95), 
                    stop:1 rgba(245, 250, 245, 0.98));
                border-radius: 15px;
                border: 2px solid rgba(144, 198, 149, 0.6);
                padding: 10px;
            }
        """)
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)
        right_layout.setContentsMargins(20, 20, 20, 20)
        
        # Recommendations title
        recommendations_title = QLabel("📊 Recommendations & Analysis")
        recommendations_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2d4a2d;
            padding: 10px 0px;
            text-align: center;
            border-bottom: 2px solid #90c695;
            margin-bottom: 15px;
        """)
        recommendations_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Output area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        
        # Improved styling for the recommendation box
        self.output_area.setStyleSheet("""
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8fff8);
                color: #2d2d2d; 
                font-size: 15px;
                font-family: 'Segoe UI', Arial, sans-serif;
                border-radius: 12px; 
                padding: 20px; 
                border: 2px solid rgba(144, 198, 149, 0.6);
                line-height: 1.6;
                selection-background-color: #c8e6c9;
            }
            QScrollBar:vertical {
                background-color: #f0f8f0;
                width: 12px;
                border-radius: 6px;
                border: 1px solid #90c695;
            }
            QScrollBar::handle:vertical {
                background-color: #90c695;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #4caf50;
            }
        """)
        
        # Enable word wrap and set proper text interaction
        self.output_area.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.output_area.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard)

        # Set initial placeholder text
        self.output_area.setHtml("""
        <div style="text-align: center; color: #888; font-style: italic; margin-top: 50px;">
            <h3>Welcome to Smart Crop Rotation Assistant! 🌾</h3>
            <p>Fill out the form on the left and click "Get Recommendations" to see personalized farming advice here.</p>
            <br>
            <p style="font-size: 14px;">Features include:</p>
            <ul style="text-align: left; max-width: 400px; margin: 0 auto;">
                <li>🔄 Crop rotation analysis</li>
                <li>🌱 Soil management recommendations</li>
                <li>🧪 Fertilizer suggestions</li>
                <li>🔬 Modern farming techniques</li>
                <li>🌾 Next crop suggestions</li>
            </ul>
        </div>
        """)

        # Assemble right panel
        right_layout.addWidget(recommendations_title)
        right_layout.addWidget(self.output_area, 1)  # Give it stretch factor
        
        right_panel.setLayout(right_layout)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        
        # Set initial sizes (30% left, 70% right)
        splitter.setSizes([400, 900])
        splitter.setCollapsible(0, False)  # Left panel can't be collapsed
        splitter.setCollapsible(1, False)  # Right panel can't be collapsed
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def handle_submit(self):
        # Clear previous content
        self.output_area.clear()
        
        # Validate size
        try:
            farmland_size = float(self.farmland_size_input.text())
            if farmland_size <= 0:
                raise ValueError
        except ValueError:
            return self.show_error("Please enter a valid farmland size (e.g., 2 or 3.5).")

        prev_name = self.previous_crop_input.currentText()
        curr_name = self.current_crop_input.currentText()
        soil_type = self.soil_type_input.currentText()

        # Objects
        prev_crop = next((c for c in CROPS if c.name == prev_name), None)
        curr_crop = next((c for c in CROPS if c.name == curr_name), None)
        soil_obj = next((s for s in SOILS if s.soil_type == soil_type), None)
        if not (prev_crop and curr_crop and soil_obj):
            return self.show_error("Invalid crop or soil selection.")

        # Rotation check
        rotation_msg, alternatives = self.rotation_logic.check_rotation(prev_name, curr_name)

        # Soil & fertilizer & techniques
        soil_rec = SoilRecommendationSystem.recommend_soil_management(soil_obj, [prev_crop, curr_crop])
        fertilizer = SoilRecommendationSystem.recommend_fertilizer(curr_name)
        techniques = TechniqueSuggestion.suggest_for_crop(curr_name)

        # Suggest next crops compatible with selected soil (and different from prev family)
        next_crops = [
            c.name for c in CROPS
            if c.family != prev_crop.family and (soil_type in c.recommended_soil)
        ]

        # Show alternatives section only if rotation is bad
        if alternatives:
            self.alternatives_widget.setVisible(True)
            # filter alternatives by soil and not same family as previous
            filtered_alts = [
                alt for alt in alternatives
                if any(cs.name == alt for cs in CROPS) and
                   next((c for c in CROPS if c.name == alt and soil_type in c.recommended_soil), None)
            ]
            # fallback to unfiltered if filtering empties
            self.alternative_combo.clear()
            self.alternative_combo.addItems(filtered_alts or alternatives)
        else:
            self.alternatives_widget.setVisible(False)

        # Generate and display recommendations
        try:
            output = self._generate_recommendation_html(
                rotation_msg, alternatives, soil_rec, fertilizer, 
                techniques, next_crops, farmland_size
            )
            self.output_area.setHtml(output)
        except Exception as e:
            # Fallback to plain text if HTML fails
            plain_text = self._generate_recommendation_text(
                rotation_msg, alternatives, soil_rec, fertilizer,
                techniques, next_crops, farmland_size
            )
            self.output_area.setPlainText(plain_text)

        # Save to DB
        try:
            self.db.save_user_entry(
                farmland_size,
                prev_name,
                curr_name,
                soil_type,
                rotation_msg,
                fertilizer,
                ", ".join(techniques) if techniques else ""
            )
        except Exception as e:
            print(f"Database error: {e}")  # For debugging

    def _generate_recommendation_html(self, rotation_msg, alternatives, soil_rec, fertilizer, techniques, next_crops, farmland_size):
        """Generate well-formatted HTML for recommendations"""
        output = []
        output.append("""
        <html>
        <head>
            <style>
                body { 
                    font-family: 'Segoe UI', Arial, sans-serif; 
                    margin: 0; 
                    padding: 0;
                    line-height: 1.8;
                    color: #2d2d2d;
                }
                .header-info {
                    background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
                    border: 2px solid #4a90e2;
                    border-radius: 10px;
                    padding: 15px;
                    margin-bottom: 20px;
                    text-align: center;
                }
                .warning-box {
                    background: linear-gradient(135deg, #fff8e1 0%, #fff3c4 100%);
                    color: #e65100;
                    padding: 15px;
                    border-radius: 10px;
                    border: 2px solid #ffcc02;
                    margin: 15px 0px;
                    box-shadow: 0px 3px 8px rgba(255,193,7,0.2);
                    font-weight: bold;
                }
                .success-box {
                    background: linear-gradient(135deg, #e8f5e8 0%, #d4f4d4 100%);
                    color: #2e7d32;
                    padding: 15px;
                    border-radius: 10px;
                    border: 2px solid #81c784;
                    margin: 15px 0px;
                    box-shadow: 0px 3px 8px rgba(129,199,132,0.2);
                    font-weight: bold;
                }
                .section {
                    margin: 20px 0px;
                    padding: 15px;
                    border-left: 4px solid #4caf50;
                    background: rgba(248, 255, 248, 0.5);
                    border-radius: 0px 8px 8px 0px;
                    box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
                }
                .section-title {
                    color: #2d4a2d;
                    font-size: 16px;
                    font-weight: bold;
                    margin-bottom: 10px;
                    display: flex;
                    align-items: center;
                }
                .section-content {
                    color: #555;
                    margin-left: 10px;
                    font-size: 14px;
                }
                .highlight {
                    background: rgba(76, 175, 80, 0.15);
                    padding: 3px 6px;
                    border-radius: 4px;
                    font-weight: 500;
                }
                .grid-container {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                    margin: 15px 0;
                }
                .stat-card {
                    background: white;
                    border: 1px solid #90c695;
                    border-radius: 8px;
                    padding: 12px;
                    text-align: center;
                    box-shadow: 0px 2px 4px rgba(0,0,0,0.1);
                }
                .techniques-grid {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                    margin-top: 10px;
                }
                .technique-tag {
                    background: linear-gradient(135deg, #4caf50, #45a049);
                    color: white;
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-size: 12px;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
        """)
        
        # Header with farm info
        output.append(f"""
        <div class="header-info">
            <h3 style="margin: 0; color: #4a90e2;">🚜 Farm Analysis Summary</h3>
            <p style="margin: 5px 0;"><strong>Farmland Size:</strong> {farmland_size} acres/hectares</p>
            <p style="margin: 5px 0;"><strong>Transition:</strong> {self.previous_crop_input.currentText()} → {self.current_crop_input.currentText()}</p>
        </div>
        """)
        
        # Rotation status
        if alternatives:
            output.append(f"""
            <div class="warning-box">
                <span style="font-size: 16px;">⚠️ Rotation Warning</span><br>
                {rotation_msg}
            </div>
            """)
        else:
            output.append(f"""
            <div class="success-box">
                <span style="font-size: 16px;">✅ Rotation Success</span><br>
                {rotation_msg}
            </div>
            """)

        # Soil Management
        if soil_rec:
            output.append(f"""
            <div class="section">
                <div class="section-title">🌱 Soil Management Strategy</div>
                <div class="section-content">{soil_rec}</div>
            </div>
            """)

        # Fertilizer
        if fertilizer:
            output.append(f"""
            <div class="section">
                <div class="section-title">🧪 Fertilizer Recommendations</div>
                <div class="section-content">{fertilizer}</div>
            </div>
            """)

        # Techniques
        if techniques:
            techniques_html = ''.join(f'<span class="technique-tag">{t}</span>' for t in techniques)
            output.append(f"""
            <div class="section">
                <div class="section-title">🔬 Modern Farming Techniques</div>
                <div class="section-content">
                    <div class="techniques-grid">{techniques_html}</div>
                </div>
            </div>
            """)

        # Next crops
        if next_crops:
            next_crops_html = ', '.join(f'<span class="highlight">{crop}</span>' for crop in next_crops)
            output.append(f"""
            <div class="section">
                <div class="section-title">🌾 Recommended Next Crops</div>
                <div class="section-content">
                    <p>Based on your soil type and crop rotation principles:</p>
                    {next_crops_html}
                </div>
            </div>
            """)
        else:
            output.append(f"""
            <div class="section">
                <div class="section-title">🌾 Recommended Next Crops</div>
                <div class="section-content">
                    <p style="color: #e65100; font-style: italic;">
                        No suitable crops found for your current soil type. 
                        Consider soil amendment or consult with local agricultural experts.
                    </p>
                </div>
            </div>
            """)
        
        # Footer
        output.append("""
        <div style="margin-top: 30px; padding: 15px; background: rgba(232, 244, 232, 0.5); 
                    border-radius: 8px; text-align: center; border: 1px dashed #90c695;">
            <p style="margin: 0; font-size: 12px; color: #666; font-style: italic;">
                💡 Tip: These recommendations are based on general agricultural principles. 
                Always consult with local agricultural extension services for region-specific advice.
            </p>
        </div>
        """)
        
        output.append("</body></html>")
        return "".join(output)

    def _generate_recommendation_text(self, rotation_msg, alternatives, soil_rec, fertilizer, techniques, next_crops, farmland_size):
        """Generate plain text fallback for recommendations"""
        output = []
        
        output.append(f"=== FARM ANALYSIS SUMMARY ===\n")
        output.append(f"Farmland Size: {farmland_size} acres/hectares\n")
        output.append(f"Crop Transition: {self.previous_crop_input.currentText()} → {self.current_crop_input.currentText()}\n\n")
        
        if alternatives:
            output.append(f"⚠️ ROTATION WARNING:\n{rotation_msg}\n\n")
        else:
            output.append(f"✅ ROTATION SUCCESS:\n{rotation_msg}\n\n")
        
        output.append(f"🌱 SOIL MANAGEMENT:\n{soil_rec}\n\n")
        output.append(f"🧪 FERTILIZER:\n{fertilizer}\n\n")
        output.append(f"🔬 MODERN TECHNIQUES:\n{', '.join(techniques) if techniques else 'None available'}\n\n")
        output.append(f"🌾 NEXT SUITABLE CROPS:\n{', '.join(next_crops) if next_crops else 'None found for current soil type'}\n\n")
        
        return "".join(output)

    def apply_alternative(self):
        alt = self.alternative_combo.currentText().strip()
        if not alt:
            return
        # set current crop to alternative and re-run
        self.current_crop_input.setCurrentText(alt)
        self.handle_submit()

    def open_logs(self):
        self.logs_window = LogsWindow(self)
        self.logs_window.show()
        self.hide()

    def show_error(self, message):
        QMessageBox.critical(self, "Input Error", message)


def main():
    app = QApplication(sys.argv)
    
    # Set application palette for better color support
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(232, 244, 232))
    app.setPalette(palette)
    
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()