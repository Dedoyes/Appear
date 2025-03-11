import sys 
from PyQt5.QtWidgets import QApplication, QColorDialog, QFileDialog, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QColorDialog, QFileDialog
from PyQt5.QtGui import QPainter, QPen, QColor, QImage, QPainterPath 
from PyQt5.QtCore import Qt, QPoint, QRect 

class Canvas (QWidget) : 
    def __init__ (self) : 
        super ().__init__ () 
        self.image = QImage (800, 600, QImage.Format_RGB32)
        self.image.fill (QColor ("white"))
        self.drawing = False 
        self.last_point = QPoint ()
        self.current_shape = "line"
        self.pen_color = QColor ("black")
        self.shapes = []

    def mousePressEvent (self, event) : 
        if event.button () == Qt.MouseButton.LeftButton: 
            self.drawing = True 
            self.last_point = event.pos ()
            self.temp_shape = {
                "type" : self.current_shape,
                "start" : event.pos (),
                "end" : event.pos (),
                "color" : self.pen_color
            }

    def mouseMoveEvent (self, event) : 
        if self.drawing : 
            self.temp_shape["end"] = event.pos ()
            self.update ()

    def mouseReleaseEvent (self, event) : 
        if event.button () == Qt.MouseButton.LeftButton : 
            self.drawing = False 
            self.shapes.append (self.temp_shape.copy ())
            self.update ()

    def paintEvent (self, event) : 
        painter = QPainter (self)
        painter.drawImage (0, 0, self.image)
        
        temp_painter = QPainter (self.image)
        for shape in self.shapes : 
            temp_painter.setPen (QPen (shape["color"], 2, Qt.PenStyle.SolidLine))
            start = shape["start"]
            end = shape["end"]
            if shape["type"] == "line" :
                temp_painter.drawLine (start, end)
            elif shape["type"] == "rect" : 
                rect = QRect (start, end)
                temp_painter.drawRect (rect)
            elif shape["type"] == "ellipse" :
                rect = QRect (start, end)
                temp_painter.drawEllipse (rect)
        temp_painter.end ()

        if self.drawing : 
            painter.setPen (QPen (self.pen_color, 2, Qt.PenStyle.SolidLine))
            start = self.temp_shape["start"]
            end = self.temp_shape["end"]
            if self.current_shape == "line" : 
                painter.drawLine (start, end)
            elif self.current_shape == "rect" : 
                painter.drawRect (QRect (start, end))
            elif self.current_shape == "ellipse" : 
                painter.drawEllipse (QRect (start, end))
            

class PaintApp (QMainWindow) : 
    def __init__ (self) : 
        super ().__init__ ()
        self.setWindowTitle ("PyQt Application")
        self.canvas = Canvas ()
        self.init_ui ()

    def init_ui (self) : 
        toolbar = QHBoxLayout ()
        btn_line = QPushButton("线条")
        btn_line.clicked.connect(lambda: self.set_tool("line"))
        btn_rect = QPushButton("矩形")
        btn_rect.clicked.connect(lambda: self.set_tool("rect"))
        btn_ellipse = QPushButton("椭圆")
        btn_ellipse.clicked.connect(lambda: self.set_tool("ellipse"))

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
            self.canvas.image.save(file_path, "PNG")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaintApp()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())








