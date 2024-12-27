from PIL import Image, ImageColor

def replace_color(image_path, output_path, original_hex, new_hex, tolerance=30):
    """
    Replace a specific color in an image with a new color, including close matches.
    Increase the tolerance parameter to tolerance for color matching

    Parameters:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        original_hex (str): Hex code of the color to replace.
        new_hex (str): Hex code of the replacement color.
        tolerance (int): Tolerance for color matching.
    """

    image = Image.open(image_path).convert("RGBA")

    original_color = ImageColor.getrgb(original_hex)
    new_color = ImageColor.getrgb(new_hex)

    pixels = image.load()
    width, height = image.size

    def is_close_color(color1, color2, tol):
        return all(abs(c1 - c2) <= tol for c1, c2 in zip(color1, color2))

    for y in range(height):
        for x in range(width):

            r, g, b, a = pixels[x, y]

            if is_close_color((r, g, b), original_color, tolerance):
                pixels[x, y] = (*new_color, a)


    image.save(output_path)

    print(f"Image saved to {output_path}")

replace_color(
    image_path="../CarsCrumbs/src/assets/logos/purple-logo.png",
    output_path="output_image.png",
    original_hex="#620086",
    new_hex="#00a6ce"
)
