# -*- coding: utf-8 -*-
# @Time   : 2025/3/11 下午10:33
# @Author : wxh
# @File   : ClickLabel.py
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
class ClickLabel(QLabel):
    click_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, QMouseEvent):
        self.click_signal.emit()

