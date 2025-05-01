from PyQt5.QtWidgets import  QFileDialog, QWidget
from PyQt5.QtGui import QPainter, QPainterPath, QPen, QColor, QImage, QPixmap 
from PyQt5.QtCore import Qt, QPoint, QRect
import os

class Canvas (QWidget) : 
    def __init__ (self) : 
        super ().__init__ () 
        self.image = QImage (1024, 1024, QImage.Format_ARGB32)
        self.image.fill (QColor ("white"))
        self.drawing = False
        self.last_point = QPoint ()
        self.current_shape = "line"
        self.pen_color = QColor ("black")
        self.pen_size = 5  # 默认画笔粗细
        self.shapes = []
        
        # 设置画布样式 - 苹果风格
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
        """)
        
        # 设置最小尺寸
        self.setMinimumSize(800, 600)
        
        # 设置鼠标追踪，以便在绘制曲线时更流畅
        self.setMouseTracking(True)

    def importJPG (self, specPath="") :
        if specPath != "" : 
            filePath = specPath
        else : 
            filePath, _ = QFileDialog.getOpenFileName (self, "选择图片", "", "Image Files (*.jpg *.png *.bmp)")
        if filePath : 
            image = QImage (filePath)
            if image.isNull () : 
                print ("错误: 加载图片失败!")
            else : 
                print ("图片加载成功。")
                pixmap = QPixmap (filePath)
                self.temp_shape = {
                    "type" : "image",
                    "image" : pixmap
                }
                self.shapes.append (self.temp_shape)

    def saveAsJPG (self) : 
        scriptDir = os.path.dirname (os.path.abspath (__file__))
        parentDir = os.path.dirname (scriptDir)
        savePath = os.path.join (parentDir, "saves")
        if not os.path.exists (savePath) : 
            os.makedirs (savePath) 
        savePath = os.path.join (savePath, "save.jpg")
        savePath = os.path.abspath (savePath)
        print (self.image.size ())
        print (savePath)
        if self.image.isNull () : 
            print ("错误: 图片为空，无法保存!")
            return 
        status = self.image.save (savePath, "JPG")
        if status : 
            print ("保存成功。")
        else :
            print ("错误: 保存失败!")

    def mousePressEvent (self, event) :
        if event.button () == Qt.MouseButton.LeftButton: 
            self.drawing = True 
            self.last_point = event.pos ()
            self.temp_shape = {
                "type" : self.current_shape,
                "start" : event.pos (),
                "end" : event.pos (),
                "color" : self.pen_color,
                "size" : self.pen_size,
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
        self.image.fill (QColor ("white"))
        temp_painter = QPainter(self.image)
        temp_painter.setPen(QPen(self.pen_color, self.pen_size, Qt.PenStyle.SolidLine))
        temp_painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 重新绘制所有永久图形
        for shape in self.shapes:
            if shape["type"] == "image" : 
                temp_painter.drawPixmap (0, 0, shape["image"])
                continue
                
            # 使用形状中保存的画笔粗细
            pen_size = shape.get("size", self.pen_size)
            temp_painter.setPen (QPen (shape["color"], pen_size, Qt.PenStyle.SolidLine))
            
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

        # 在 widget 上绘制最终图像
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawImage(0, 0, self.image)

        # 如果正在绘制，则额外绘制临时图形（用于预览）
        if self.drawing:
            painter.setPen(QPen(self.pen_color, self.pen_size, Qt.PenStyle.SolidLine))
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




