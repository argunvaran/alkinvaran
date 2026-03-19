from PIL import Image
import os

def remove_background():
    img_path = r"c:\Kutum\alkin\static\favicon.png"
    if not os.path.exists(img_path):
        print("Image not found")
        return
        
    img = Image.open(img_path).convert("RGBA")
    datas = img.getdata()
    
    # We want to replace very dark pixels with transparent ones
    # Threshold for black (tolerance up to 25/255)
    newData = []
    for item in datas:
        if item[0] < 25 and item[1] < 25 and item[2] < 25:
            # Fully transparent
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
            
    img.putdata(newData)
    img.save(img_path, "PNG")
    print("Background successfully removed!")

if __name__ == "__main__":
    remove_background()
