from PyQt5.QtWidgets import  QWidget
from PyQt5.QtGui import QPainter, QPainterPath, QPen, QColor, QImage 
from PyQt5.QtCore import Qt, QPoint, QRect 

class Canvas (QWidget) : 
    def __init__ (self) : 
        super ().__init__ () 
        self.image = QImage (1920, 1080, QImage.Format_ARGB32)
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
                "color" : self.pen_color,
                "curve" : [event.pos ()]
            }
            self.update ()

    def mouseMoveEvent (self, event) : 
        if self.drawing : 
            self.temp_shape["end"] = event.pos ()
            if self.temp_shape["type"] == "curve" : 
                self.temp_shape["curve"].append (event.pos ())
            self.update ()

    def mouseReleaseEvent (self, event) : 
        if event.button () == Qt.MouseButton.LeftButton : 
            self.drawing = False 
            self.shapes.append (self.temp_shape.copy ())
            self.update ()

    def paintEvent (self, event) :
            # 先重新填充白色，重置画布
        self.image.fill(QColor("white"))
        temp_painter = QPainter(self.image)
        temp_painter.setPen(QPen(self.pen_color, 5, Qt.PenStyle.SolidLine))
        temp_painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # 重新绘制所有永久图形
        for shape in self.shapes:
            temp_painter.setPen (QPen (shape["color"], 5, Qt.PenStyle.SolidLine))
            start = shape["start"]
            end = shape["end"]
            if shape["type"] == "line":
                temp_painter.drawLine(start, end)
            elif shape["type"] == "rect":
                temp_painter.drawRect(QRect(start, end))
            elif shape["type"] == "ellipse":
                temp_painter.drawEllipse(QRect(start, end))
            elif shape["type"] == "curve":
                path = QPainterPath()
                path.moveTo(shape["curve"][0])
                for point in shape["curve"][1:]:
                    path.lineTo(point)
                temp_painter.drawPath(path)
        temp_painter.end()

    # 再在 widget 上绘制最终图像
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawImage(0, 0, self.image)

    # 如果正在绘制，则额外绘制临时图形（用于预览）
        if self.drawing:
            painter.setPen(QPen(self.pen_color, 5, Qt.PenStyle.SolidLine))
            start = self.temp_shape["start"]
            end = self.temp_shape["end"]
            if self.current_shape == "line":
                painter.drawLine(start, end)
            elif self.current_shape == "rect":
                painter.drawRect(QRect(start, end))
            elif self.current_shape == "ellipse":
                painter.drawEllipse(QRect(start, end))
            elif self.current_shape == "curve":
                path = QPainterPath()
                path.moveTo(self.temp_shape["curve"][0])
                for point in self.temp_shape["curve"][1:]:
                    path.lineTo(point)
                painter.drawPath(path)
