from PyQt5.QtWidgets import QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont

class TitleSection:
    """Title section component that displays the application name."""
    
    def __init__(self, parent):
        """Initialize the title section."""
        self.layout = QHBoxLayout()
        self._create_title()
        
    def _create_title(self):
        """Create and setup the title label."""
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        title_label = QLabel("Glimmer")
        title_label.setFont(QFont("Arial", 18))
        title_label.setStyleSheet("color: rgb(230, 180, 255);")
        title_label.setFixedHeight(50)  # Example height, adjust as needed
        self.layout.addSpacerItem(spacer)
        self.layout.addWidget(title_label)
        self.layout.addSpacerItem(spacer)