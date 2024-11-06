from PyQt5.QtWidgets import QLabel, QVBoxLayout, QSlider, QGroupBox
from PyQt5.QtCore import Qt, QObject

class SliderSection:
    """Slider section component that contains all brightness control sliders."""

    def __init__(self, parent):
        self.parent = parent
        self.layout = QVBoxLayout()
        self._create_sliders()

    def _create_sliders(self):
        self.group = QGroupBox("Brightness Control")
        slider_layout = QVBoxLayout()

        self.manual_brightness_label = QLabel("Manual Brightness")
        self.manual_brightness_label.setStyleSheet("color: rgb(230, 180, 255);")
        self.manual_brightness_slider = QSlider(Qt.Horizontal)
        self.manual_brightness_slider.setRange(0, 100)
        self.manual_brightness_slider.setValue(80)

        self.sensitivity_slider, self.sensitivity_label = self._create_slider("Sensitivity", 1, 10, 7)
        self.max_brightness_slider, self.max_brightness_label = self._create_slider("Maximum Brightness", 0, 100, 80)
        self.min_brightness_slider, self.min_brightness_label = self._create_slider("Minimum Brightness", 0, 100, 20)

        self.manual_brightness_slider.setVisible(False)
        self.manual_brightness_label.setVisible(False)

        self.manual_brightness_slider.valueChanged.connect(self.parent.set_manual_brightness)
        self.min_brightness_slider.valueChanged.connect(self._ensure_min_max_order)
        self.max_brightness_slider.valueChanged.connect(self._ensure_min_max_order)

        slider_layout.addWidget(self.manual_brightness_label)
        slider_layout.addWidget(self.manual_brightness_slider)
        slider_layout.addWidget(self.sensitivity_label)
        slider_layout.addWidget(self.sensitivity_slider)
        slider_layout.addWidget(self.max_brightness_label)
        slider_layout.addWidget(self.max_brightness_slider)
        slider_layout.addWidget(self.min_brightness_label)
        slider_layout.addWidget(self.min_brightness_slider)

        self.group.setLayout(slider_layout)
        self.group.setStyleSheet("color: rgb(230, 180, 255);")
        self.group.setFixedHeight(200)

        self.layout.addWidget(self.group)

    def _create_slider(self, label_text, min_val, max_val, default_val):
        slider_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("color: rgb(230, 180, 255);")

        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(default_val)

        slider_layout.addWidget(label)
        slider_layout.addWidget(slider)

        return slider, label

    def _ensure_min_max_order(self, value):
        min_value = self.min_brightness_slider.value()
        max_value = self.max_brightness_slider.value()

        if min_value > max_value:
            if value == self.min_brightness_slider.value():
                self.min_brightness_slider.setValue(max_value)
            else:
                self.max_brightness_slider.setValue(min_value)

    def show_automatic_controls(self):
        self.sensitivity_slider.setVisible(True)
        self.sensitivity_label.setVisible(True)
        self.max_brightness_slider.setVisible(True)
        self.max_brightness_label.setVisible(True)
        self.min_brightness_slider.setVisible(True)
        self.min_brightness_label.setVisible(True)
        self.manual_brightness_slider.setVisible(False)
        self.manual_brightness_label.setVisible(False)

    def show_manual_controls(self):
        self.sensitivity_slider.setVisible(False)
        self.sensitivity_label.setVisible(False)
        self.max_brightness_slider.setVisible(False)
        self.max_brightness_label.setVisible(False)
        self.min_brightness_slider.setVisible(False)
        self.min_brightness_label.setVisible(False)
        self.manual_brightness_slider.setVisible(True)
        self.manual_brightness_label.setVisible(True)
        self.group.setFixedHeight(150)
