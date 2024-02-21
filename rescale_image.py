"""
Rescales and saves an image.
"""

from PIL import Image

img = Image.open('original_image.jpg')

# (Width, Height)
new_size = (2010, 634)

img_rescaled = img.resize(new_size, Image.LANCZOS)

img_rescaled.save('rescaled_image.jpg')

print("Image has been rescaled successfully!")
