from PIL import Image, ImageDraw


def create_image_char(size, background, character, char_color, char_pos, char_font):
    """Create a PIL image object of specified size and color that has the provided character \
    in."""
    image = Image.new("RGBA", size, background)
    draw = ImageDraw.Draw(image)
    draw.text(char_pos, character, fill=char_color, font=char_font)
    return image
