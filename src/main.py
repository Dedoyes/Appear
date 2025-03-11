import PaintApp
import sys 
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaintApp.PaintApp()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())








