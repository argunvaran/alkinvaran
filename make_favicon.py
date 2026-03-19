import os
from PIL import Image, ImageDraw, ImageFont

def generate():
    size = 512
    # Background: Transparent or very dark grey (primary color of the site is #0a0a0a)
    bg_color = (10, 10, 10, 255)
    img = Image.new('RGBA', (size, size), bg_color)
    draw = ImageDraw.Draw(img)

    # Pick a robust clean font present on Windows
    font_paths = [
        "C:/Windows/Fonts/bahnschrift.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf"
    ]
    font_path = None
    for p in font_paths:
        if os.path.exists(p):
            font_path = p
            break

    if not font_path:
        print("No suitable font found!")
        return

    # Start with a very large font size and scale dynamically to fill the box
    font_size = 600
    font = ImageFont.truetype(font_path, font_size)

    # We want merged A and V (Monogram style)
    text_a = "A"
    text_v = "V"

    bbox_A = draw.textbbox((0, 0), text_a, font=font)
    bbox_V = draw.textbbox((0, 0), text_v, font=font)
    
    w_A = bbox_A[2] - bbox_A[0]
    w_V = bbox_V[2] - bbox_V[0]
    
    # Negative gap forces them to overlap and merge!
    # A's right leg tilts down-right, V's left leg tilts down-right.
    # We overlap them to form a cohesive, woven-looking geometric logo.
    gap = -int(w_A * 0.45) 
    
    total_w = w_A + gap + w_V
    
    # Target width is 80% of the total image for maximum visibility as a favicon
    target_w = size * 0.80
    
    # Scale down or up to fit perfectly
    scale_factor = target_w / total_w
    font_size = int(font_size * scale_factor)
    
    # Re-evaluate with the perfect font size
    font = ImageFont.truetype(font_path, font_size)
    bbox_A = draw.textbbox((0, 0), text_a, font=font)
    bbox_V = draw.textbbox((0, 0), text_v, font=font)
    
    w_A = bbox_A[2] - bbox_A[0]
    w_V = bbox_V[2] - bbox_V[0]
    gap = -int(w_A * 0.45)
    total_w = w_A + gap + w_V
    
    h_A = bbox_A[3] - bbox_A[1]
    h_V = bbox_V[3] - bbox_V[1]
    max_h = max(h_A, h_V)
    
    # Center mathematically
    x_start = (size - total_w) / 2
    y_start = (size - max_h) / 2 - min(bbox_A[1], bbox_V[1])

    # Draw 'A' in pure white
    draw.text((x_start - bbox_A[0], y_start), text_a, font=font, fill=(255, 255, 255, 255))
    
    # Draw 'V' in Accent Blue (#3b82f6), layered on top to merge them!
    # Giving it a SLIGHT transparency lets the white 'A' shine through making them physically combined!
    x_v = x_start + w_A + gap - bbox_V[0]
    draw.text((x_v, y_start), text_v, font=font, fill=(59, 130, 246, 230))

    img.save(r"c:\Kutum\alkin\static\favicon.png", "PNG")
    print("Merged Monogram Favicon created successfully!")

if __name__ == "__main__":
    generate()
