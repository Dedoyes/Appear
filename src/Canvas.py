from PyQt5.QtWidgets import  QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QImage 
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
            

