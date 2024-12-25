from PIL import Image
from collections import Counter

def get_color_codes(image_path, num_colors=3):
    try:
        with Image.open(image_path) as img:
            img = img.resize((100, 100))
            img = img.convert("RGB")
            pixels = list(img.getdata())
        
            color_counts = Counter(pixels)
            
            most_common_colors = color_counts.most_common(num_colors)
            
            color_codes = [
                (f"#{r:02x}{g:02x}{b:02x}", count) 
                for (r, g, b), count in most_common_colors
            ]
            
            return color_codes
    except Exception as e:
        print(f"Error processing image: {e}")
        return []
    

print(get_color_codes("src/assets/logos/yellow-square-logo.png"))