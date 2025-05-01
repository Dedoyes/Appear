import PaintApp
import sys 
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from pix2pix import train
if __name__ == "__main__":
    windowWidth = 1024
    windowHeight = 1024
    app = QApplication(sys.argv)

    # 设置应用程序样式
    app.setStyle("Fusion")

    # 设置应用程序字体 - 苹果风格
    font = QFont("SF Pro Text", 10)
    app.setFont(font)

    # 设置应用程序样式表
    app.setStyleSheet("""
        QApplication {
            background-color: #f5f5f5;
        }
        QMainWindow {
            background-color: #f5f5f5;
        }
        QToolBar {
            background-color: #ffffff;
            border-bottom: 1px solid #e0e0e0;
            spacing: 10px;
            padding: 5px;
        }
        QToolButton {
            background-color: transparent;
            border: none;
            border-radius: 4px;
            padding: 8px;
            color: #333333;
        }
        QToolButton:hover {
            background-color: #e0e0e0;
        }
        QToolButton:pressed {
            background-color: #d0d0d0;
        }
        QToolButton:checked {
            background-color: #d0d0d0;
        }
        QLabel {
            font-weight: bold;
            color: #333333;
        }
        QSpinBox {
            padding: 5px;
            border: 1px solid #cccccc;
            border-radius: 4px;
            background-color: white;
        }
    """)

    # 创建并显示主窗口
    window = PaintApp.PaintApp()
    window.resize(windowWidth, windowHeight)
    window.setWindowTitle("Appear - 智能绘图工具")
    window.show()

    sys.exit(app.exec_())








