# Guarda esto como: create_icon.py
from PIL import Image, ImageDraw
import os

# Crear ícono en varios tamaños
sizes = [16, 32, 48, 64, 128, 256]
images = []

for size in sizes:
    # Crear imagen con fondo transparente
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Dibujar el ícono de power
    padding = size // 8
    circle_bounds = [padding, padding, size-padding, size-padding]
    
    # Círculo exterior
    draw.ellipse(circle_bounds, fill=(31, 83, 141), outline=(255, 255, 255))
    
    # Línea vertical del power
    line_width = size // 16
    line_x = size // 2
    line_y1 = size // 4
    line_y2 = size // 2
    draw.rectangle([line_x - line_width//2, line_y1, line_x + line_width//2, line_y2], 
                   fill=(255, 255, 255))
    
    # Arco del power
    arc_padding = size // 4
    arc_bounds = [arc_padding, arc_padding, size-arc_padding, size-arc_padding]
    draw.arc(arc_bounds, start=45, end=315, fill=(255, 255, 255), width=line_width)
    
    images.append(img)

# Guardar como .ico
images[0].save('shutdown_timer.ico', format='ICO', sizes=[(s, s) for s in sizes])
print("Ícono creado: shutdown_timer.ico")