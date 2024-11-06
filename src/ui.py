from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QDesktopWidget, QSystemTrayIcon, QMessageBox
from PyQt5.QtCore import QTimer
import sys
from PyQt5.QtCore import Qt
from controllers.brightness_controller import BrightnessController
from components import TitleSection, ButtonSection, SliderSection, StatusSection
from utils.window_manager import WindowManager
from utils.styles import StyleManager

class UI(QMainWindow):
    THEMES = {
        "Outdoor": (100, 50),
        "Indoor": (50, 10)
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Glimmer")
        self.setFixedSize(500, 600)
        self.center()
        self.theme = "Indoor"
        self.brightness_controller = BrightnessController()
        
        # Check if system tray is available
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(None, "Glimmer",
                               "System tray is not available on this system")
            sys.exit(1)
            
        # Initialize window manager before UI components
        self.window_manager = WindowManager(self)
        
        self.init_ui()
        
        # Set window flags to keep it above others when restored
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_ui(self):
        # Set up main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Initialize components
        self.title_section = TitleSection(self)
        self.button_section = ButtonSection(self)
        self.slider_section = SliderSection(self)
        self.status_section = StatusSection()

        # Add components to main layout
        self.layout.addLayout(self.title_section.layout)
        self.layout.addLayout(self.button_section.layout)
        self.layout.addLayout(self.slider_section.layout)
        self.layout.addLayout(self.status_section.layout)

        # Set up timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_brightness)
        self.timer.start(1000)

        # Apply styles
        self.setStyleSheet(StyleManager.get_theme_styles())

    def closeEvent(self, event):
        event.ignore()
        self.window_manager.minimize()

    def set_theme(self, theme):
        self.theme = theme
        max_brightness, min_brightness = self.THEMES[theme]
        self.slider_section.max_brightness_slider.setValue(max_brightness)
        self.slider_section.min_brightness_slider.setValue(min_brightness)
        self.brightness_controller.set_brightness_limits(max_brightness, min_brightness)

    def update_brightness(self):
        avg_brightness, target_brightness = self.brightness_controller.adjust_brightness(
            sensitivity=self.slider_section.sensitivity_slider.value(),
            max_brightness=self.slider_section.max_brightness_slider.value(),
            min_brightness=self.slider_section.min_brightness_slider.value()
        )
        self.status_section.status_label.setText(
            f"Average Brightness: {avg_brightness:.2f}\n"
            f"Adjusted Brightness: {target_brightness:.2f}%"
        )

    def toggle_pause(self):
        if self.brightness_controller.paused:
            self.resume_automatic_control()
        else:
            self.pause_automatic_control()

    def resume_automatic_control(self):
        self.brightness_controller.resume()
        self.button_section.pause_button.setText("Pause")
        self._toggle_slider_visibility(True)

    def pause_automatic_control(self):
        self.brightness_controller.pause()
        self.button_section.pause_button.setText("Resume")
        self._toggle_slider_visibility(False)

    def _toggle_slider_visibility(self, show_automatic):
        # Toggle visibility of automatic control sliders
        self.slider_section.sensitivity_slider.setVisible(show_automatic)
        self.slider_section.sensitivity_label.setVisible(show_automatic)
        self.slider_section.max_brightness_slider.setVisible(show_automatic)
        self.slider_section.max_brightness_label.setVisible(show_automatic)
        self.slider_section.min_brightness_slider.setVisible(show_automatic)
        self.slider_section.min_brightness_label.setVisible(show_automatic)
        
        # Toggle visibility of manual brightness slider
        self.slider_section.manual_brightness_slider.setVisible(not show_automatic)
        self.slider_section.manual_brightness_label.setVisible(not show_automatic)

    def set_manual_brightness(self, value):
        self.brightness_controller.set_manual_brightness(value)