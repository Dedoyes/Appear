import os
from PIL import Image, ImageDraw

# 确保图标目录存在
icon_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
if not os.path.exists(icon_dir):
    os.makedirs(icon_dir)

# 定义图标尺寸
icon_size = 24

# 定义颜色
colors = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 59, 48, 255),
    "blue": (0, 122, 255, 255),
    "green": (52, 199, 89, 255),
    "gray": (142, 142, 147, 255),
    "light_gray": (229, 229, 231, 255)
}

# 创建线条图标
def create_line_icon():
    img = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 绘制一条直线
    draw.line([(4, 12), (20, 12)], fill=colors["black"], width=2)
    img.save(os.path.join(icon_dir, "line.png"))

# 创建矩形图标
def create_rect_icon():
    img = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 绘制一个矩形
    draw.rectangle([(4, 4), (20, 20)], outline=colors["black"], width=2)
    img.save(os.path.join(icon_dir, "rect.png"))

# 创建椭圆图标
def create_ellipse_icon():
    img = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 绘制一个椭圆
    draw.ellipse([(4, 4), (20, 20)], outline=colors["black"], width=2)
    img.save(os.path.join(icon_dir, "ellipse.png"))

# 创建曲线图标
def create_curve_icon():
    img = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 绘制一条曲线
    points = [(4, 20), (8, 8), (12, 16), (16, 4), (20, 12)]
    draw.line(points, fill=colors["black"], width=2)
    img.save(os.path.join(icon_dir, "curve.png"))

# 创建颜色图标
def create_color_icon():
    img = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 绘制一个颜色选择器图标
    draw.rectangle([(4, 4), (20, 20)], fill=colors["red"])
    draw.rectangle([(8, 8), (16, 16)], fill=colors["blue"])
    img.save(os.path.join(icon_dir, "color.png"))

# 创建清空图标
def create_clear_icon():
    img = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 绘制一个清空图标
    draw.rectangle([(4, 4), (20, 20)], fill=colors["white"])
    draw.line([(6, 6), (18, 18)], fill=colors["black"], width=2)
    draw.line([(6, 18), (18, 6)], fill=colors["black"], width=2)
    img.save(os.path.join(icon_dir, "clear.png"))

# 创建保存图标
def create_save_icon():
    img = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 绘制一个保存图标
    draw.rectangle([(4, 4), (20, 20)], outline=colors["black"], width=2)
    draw.rectangle([(6, 6), (18, 10)], fill=colors["black"])
    draw.line([(8, 12), (16, 12)], fill=colors["black"], width=2)
    draw.line([(8, 16), (16, 16)], fill=colors["black"], width=2)
    img.save(os.path.join(icon_dir, "save.png"))

# 创建重绘图标
def create_redraw_icon():
    img = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 绘制一个重绘图标
    draw.ellipse([(4, 4), (20, 20)], outline=colors["black"], width=2)
    draw.line([(12, 4), (12, 20)], fill=colors["black"], width=2)
    draw.line([(4, 12), (20, 12)], fill=colors["black"], width=2)
    # 添加一个箭头
    draw.polygon([(16, 8), (20, 12), (16, 16)], fill=colors["black"])
    img.save(os.path.join(icon_dir, "redraw.png"))

# 创建导入图标
def create_import_icon():
    img = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 绘制一个导入图标
    draw.rectangle([(4, 4), (20, 20)], outline=colors["black"], width=2)
    draw.line([(12, 4), (12, 20)], fill=colors["black"], width=2)
    draw.polygon([(8, 8), (12, 4), (16, 8)], fill=colors["black"])
    img.save(os.path.join(icon_dir, "import.png"))

# 创建所有图标
def create_all_icons():
    create_line_icon()
    create_rect_icon()
    create_ellipse_icon()
    create_curve_icon()
    create_color_icon()
    create_clear_icon()
    create_save_icon()
    create_redraw_icon()
    create_import_icon()
    print("所有图标已创建完成！")

if __name__ == "__main__":
    create_all_icons() 