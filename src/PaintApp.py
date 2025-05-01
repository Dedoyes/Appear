import Canvas 
from PyQt5.QtWidgets import QColorDialog, QFileDialog, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QColorDialog, QFileDialog, QToolBar, QAction, QLabel, QSpinBox, QToolButton
from PyQt5.QtGui import QColor, QIcon, QFont
from PyQt5.QtCore import Qt, QSize
import os 
import sys 

PaintAppFilePath = os.path.abspath (__file__)
parentPaintAppFilePath = os.path.dirname (PaintAppFilePath)
grandparentPaintAppFilePath = os.path.dirname (parentPaintAppFilePath)
pix2pixPath = os.path.join (grandparentPaintAppFilePath, "pix2pix")
sys.path.append (pix2pixPath)
import train

class PaintApp (QMainWindow) : 
    def __init__ (self) : 
        super ().__init__ ()
        self.setWindowTitle ("Appear - 智能绘图工具")
        self.setStyleSheet("""
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
            QPushButton {
                background-color: #4a86e8;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a76d8;
            }
            QPushButton:pressed {
                background-color: #2a66c8;
            }
            QPushButton#colorBtn {
                background-color: #ff0000;
            }
            QPushButton#colorBtn:hover {
                background-color: #cc0000;
            }
            QPushButton#colorBtn:pressed {
                background-color: #990000;
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
        
        # 获取图标目录的绝对路径
        self.icon_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
        
        self.canvas = Canvas.Canvas ()
        self.init_ui ()
        
        # 当前选中的工具
        self.current_tool = None

    def init_ui (self) : 
        # 创建工具栏
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # 绘图工具组
        toolbar.addWidget(QLabel("绘图工具:"))
        
        # 创建工具按钮
        btn_line = QToolButton()
        btn_line.setIcon(QIcon(os.path.join(self.icon_dir, "line.png")))
        btn_line.setToolTip("绘制直线")
        btn_line.setCheckable(True)
        btn_line.clicked.connect(lambda: self.set_tool("line", btn_line))
        
        btn_rect = QToolButton()
        btn_rect.setIcon(QIcon(os.path.join(self.icon_dir, "rect.png")))
        btn_rect.setToolTip("绘制矩形")
        btn_rect.setCheckable(True)
        btn_rect.clicked.connect(lambda: self.set_tool("rect", btn_rect))
        
        btn_ellipse = QToolButton()
        btn_ellipse.setIcon(QIcon(os.path.join(self.icon_dir, "ellipse.png")))
        btn_ellipse.setToolTip("绘制椭圆")
        btn_ellipse.setCheckable(True)
        btn_ellipse.clicked.connect(lambda: self.set_tool("ellipse", btn_ellipse))
        
        btn_curve = QToolButton()
        btn_curve.setIcon(QIcon(os.path.join(self.icon_dir, "curve.png")))
        btn_curve.setToolTip("绘制曲线")
        btn_curve.setCheckable(True)
        btn_curve.clicked.connect(lambda: self.set_tool("curve", btn_curve))
        
        # 添加绘图工具到工具栏
        toolbar.addWidget(btn_line)
        toolbar.addWidget(btn_rect)
        toolbar.addWidget(btn_ellipse)
        toolbar.addWidget(btn_curve)
        
        # 添加分隔符
        toolbar.addSeparator()
        
        # 颜色选择
        toolbar.addWidget(QLabel("颜色:"))
        btn_color = QToolButton()
        btn_color.setIcon(QIcon(os.path.join(self.icon_dir, "color.png")))
        btn_color.setToolTip("选择绘图颜色")
        btn_color.clicked.connect(self.choose_color)
        toolbar.addWidget(btn_color)
        
        # 画笔粗细
        toolbar.addWidget(QLabel("画笔粗细:"))
        pen_size_spin = QSpinBox()
        pen_size_spin.setRange(1, 20)
        pen_size_spin.setValue(5)
        pen_size_spin.valueChanged.connect(self.set_pen_size)
        toolbar.addWidget(pen_size_spin)
        
        # 添加分隔符
        toolbar.addSeparator()
        
        # 文件操作
        toolbar.addWidget(QLabel("文件操作:"))
        
        btn_clear = QToolButton()
        btn_clear.setIcon(QIcon(os.path.join(self.icon_dir, "clear.png")))
        btn_clear.setToolTip("清空画布")
        btn_clear.clicked.connect(self.clear_canvas)
        
        btn_save = QToolButton()
        btn_save.setIcon(QIcon(os.path.join(self.icon_dir, "save.png")))
        btn_save.setToolTip("保存图像")
        btn_save.clicked.connect(self.save_image)
        
        btn_redraw = QToolButton()
        btn_redraw.setIcon(QIcon(os.path.join(self.icon_dir, "redraw.png")))
        btn_redraw.setToolTip("使用AI重绘图像")
        btn_redraw.clicked.connect(self.redraw)
        
        btn_import = QToolButton()
        btn_import.setIcon(QIcon(os.path.join(self.icon_dir, "import.png")))
        btn_import.setToolTip("导入图像")
        btn_import.clicked.connect(self.importJPG)
        
        # 添加文件操作按钮到工具栏
        toolbar.addWidget(btn_clear)
        toolbar.addWidget(btn_save)
        toolbar.addWidget(btn_redraw)
        toolbar.addWidget(btn_import)
        
        # 设置中央窗口
        self.setCentralWidget(self.canvas)
        
        # 保存工具按钮引用
        self.tool_buttons = {
            "line": btn_line,
            "rect": btn_rect,
            "ellipse": btn_ellipse,
            "curve": btn_curve
        }

    def set_tool(self, tool, button):
        # 取消之前选中的工具
        if self.current_tool and self.current_tool in self.tool_buttons:
            self.tool_buttons[self.current_tool].setChecked(False)
        
        # 设置新工具
        self.canvas.current_shape = tool
        self.current_tool = tool
        button.setChecked(True)

    def set_pen_size(self, size):
        self.canvas.pen_size = size

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.pen_color = color

    def clear_canvas(self):
        self.canvas.image.fill(QColor ("white"))
        self.canvas.shapes = []
        self.canvas.update()

    def save_image(self):
        self.canvas.saveAsJPG ()
    
    def redraw (self) : 
        self.canvas.saveAsJPG ()
        train.draw ()
        srcPath = os.path.dirname (os.path.abspath (__file__))
        basePath = os.path.dirname (srcPath)
        savesPath = os.path.join (basePath, "saves")
        objectiveFilePath = os.path.join (savesPath, "gene.jpg")
        self.canvas.importJPG (objectiveFilePath)
        self.canvas.update ()

    def importJPG (self) : 
        self.canvas.importJPG ()
        self.canvas.update ()
