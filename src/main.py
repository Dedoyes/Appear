import PaintApp
import sys 
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    windowWidth = 1024
    windowHeight = 1024
    app = QApplication(sys.argv)
    window = PaintApp.PaintApp()
    window.resize(windowWidth, windowHeight)
    window.show()
    sys.exit(app.exec_())








