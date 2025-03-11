# -*- coding: utf-8 -*-
# @Time   : 2025/3/11 下午10:21
# @Author : wxh
# @File   : MainView.py
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PaintApp import PaintApp
from ClickLabel import ClickLabel
class MainView(QWidget):
    def __init__(self, w=700, h=400):
        super().__init__()
        self.w = w
        self.h = h
        self.resize(self.w, self.h)
        self.init_control()
    def init_control(self):
        self.totalLayout = QVBoxLayout()
        self.setLayout(self.totalLayout)

        self.layout1 = QHBoxLayout()
        self.totalLayout.addLayout(self.layout1)
        self.btn = QPushButton("test")

        self.layout1.addWidget(self.btn)
        self.catalog = QComboBox(self)
        self.catalog.addItem('--请选择--')
        self.catalog.addItem('文件')
        self.catalog.addItem('新建')
        self.catalog.addItems(['保存'])
        self.layout1.addWidget(self.catalog)
        self.testLabel = ClickLabel()
        self.testLabel.setPixmap(QPixmap('../picture/icon.png'))
        self.testLabel2 = ClickLabel()
        self.testLabel2.setPixmap(QPixmap('../picture/photo4.png'))
        self.layout1.addWidget(self.testLabel)
        self.layout1.addWidget(self.testLabel2)

        self.layout2 = QHBoxLayout()
        self.totalLayout.addLayout(self.layout2)
        self.paint = PaintApp()
        self.layout2.addWidget(self.paint)
        self.testLabel.click_signal.connect(self.click_test)
        self.testLabel2.click_signal.connect(self.click_test2)

    def click_test(self):
        print('touch')

    def click_test2(self):
        print('test2')