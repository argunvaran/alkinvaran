from PIL import Image

def crop_transparent(img_path):
    img = Image.open(img_path).convert("RGBA")
    # Get bounding box of non-zero elements
    bbox = img.getbbox()
    if bbox:
        # Provide a small 5 pixel padding so it's not touching the absolute edges
        padding = 5
        left = max(0, bbox[0] - padding)
        upper = max(0, bbox[1] - padding)
        right = min(img.width, bbox[2] + padding)
        lower = min(img.height, bbox[3] + padding)
        
        cropped = img.crop((left, upper, right, lower))
        cropped.save(img_path, "PNG")
        print(f"Cropped successfully from {img.width}x{img.height} to {right-left}x{lower-upper}")
    else:
        print("Image is entirely empty?")

if __name__ == "__main__":
    crop_transparent(r"c:\Kutum\alkin\static\favicon.png")
