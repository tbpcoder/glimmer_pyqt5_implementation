# main.py
from PyQt5.QtWidgets import QApplication
import sys
from ui import UI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = UI()
    main_window.show()
    sys.exit(app.exec_())
