import Canvas 
from PyQt5.QtWidgets import QColorDialog, QFileDialog, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QColorDialog, QFileDialog
from PyQt5.QtGui import QColor 

class PaintApp (QMainWindow) : 
    def __init__ (self) : 
        super ().__init__ ()
        self.setWindowTitle ("PyQt Application")
        self.canvas = Canvas.Canvas ()
        self.init_ui ()

    def init_ui (self) : 
        toolbar = QHBoxLayout ()
        btn_line = QPushButton("线条")
        btn_line.clicked.connect(lambda: self.set_tool("line"))
        btn_rect = QPushButton("矩形")
        btn_rect.clicked.connect(lambda: self.set_tool("rect"))
        btn_ellipse = QPushButton("椭圆")
        btn_ellipse.clicked.connect(lambda: self.set_tool("ellipse"))
        btn_curve = QPushButton ("Curve")
        btn_curve.clicked.connect (lambda: self.set_tool("curve"))

        # 颜色选择
        btn_color = QPushButton("选择颜色")
        btn_color.clicked.connect(self.choose_color)
 
        # 清空和保存
        btn_clear = QPushButton("清空")
        btn_clear.clicked.connect(self.clear_canvas)
        btn_save = QPushButton("保存")
        btn_save.clicked.connect(self.save_image)
        
        # 添加按钮到工具栏
        toolbar.addWidget(btn_line)
        toolbar.addWidget(btn_rect)
        toolbar.addWidget(btn_ellipse)
        toolbar.addWidget(btn_curve)
        toolbar.addWidget(btn_color)
        toolbar.addWidget(btn_clear)
        toolbar.addWidget(btn_save)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addLayout(toolbar)
        main_layout.addWidget(self.canvas)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def set_tool(self, tool):
        self.canvas.current_shape = tool

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.pen_color = color

    def clear_canvas(self):
        self.canvas.image.fill(QColor ("white"))
        self.canvas.shapes = []
        self.canvas.update()

    def save_image(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存图片", "", "PNG Image (*.png)")
        if file_path:
            print ("save Path : ", file_path)
            self.canvas.image.save(file_path, "PNG")


