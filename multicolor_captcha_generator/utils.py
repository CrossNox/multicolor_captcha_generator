from os import path
from random import choice, randint
from PIL import ImageFont
from .constants import DEFAULT_FONT
from pkg_resources import resource_listdir, resource_string, iter_entry_points, resource_filename


def color_is_dark(r, g, b):
    """Determine if a provided color has a dark tonality."""
    # Medium tonality for RGB in 0-255 range -> (255/2)*3 = 384
    return r + g + b < 384


def color_dark_level(r, g, b):
    """Determine provided color dark tonality level from -3 to 3 (-3 ultra light, \
       -2 mid light, -1 low light, 1 low dark, 2 mid dark, 3 high dark)."""
    color_sum = r + g + b
    if color_sum > 640:
        return -3
    elif color_sum > 512:
        return -2
    elif color_sum > 384:
        return -1
    elif color_sum >= 255:
        return 1
    elif color_sum >= 128:
        return 2
    else:
        return 3


def gen_rand_font():
    """Pick a random font file path from provided folder
       and given possible fonts list."""
    fonts_list = [x for x in resource_listdir('multicolor_captcha_generator','fonts/freefont-20120503/')
                    if x.endswith(".ttf")]
    return choice(fonts_list)


def gen_rand_size_font(font_path, min_size, max_size):
    """Generate a random size font PIL object from the given font file path."""
    font_size = randint(min_size, max_size)
    font_path = "fonts/freefont-20120503/{}".format(font_path)
    try:
        font = ImageFont.truetype(resource_filename('multicolor_captcha_generator', font_path), font_size)
    except OSError:
        print("Incompatible font for captcha. Using default_font")
        font = ImageFont.truetype(DEFAULT_FONT, font_size)
    return font


def gen_rand_color(min_val=0, max_val=255):
    """Generate a random color."""
    gen_color = {"color": "", "R": -1, "G": -1, "B": -1}
    gen_color["R"] = randint(min_val, max_val)
    gen_color["G"] = randint(min_val, max_val)
    gen_color["B"] = randint(min_val, max_val)
    gen_color["color"] = "rgb({}, {}, {})".format(str(gen_color["R"]),
                                                  str(gen_color["G"]),
                                                  str(gen_color["B"]))
    return gen_color


def gen_rand_contrast_color(from_color):
    """Generate a random dark or light color for a exact contrast."""
    dark_level = color_dark_level(
        from_color["R"], from_color["G"], from_color["B"])
    color = "rgb(0, 0, 0)"
    if dark_level == -3:
        color = gen_rand_color(0, 42)
    elif dark_level == -2:
        color = gen_rand_color(42, 84)
    elif dark_level == -1:
        color = gen_rand_color(84, 126)
    elif dark_level == 1:
        color = gen_rand_color(126, 168)
    elif dark_level == 2:
        color = gen_rand_color(168, 210)
    elif dark_level == 3:
        color = gen_rand_color(210, 255)
    return color


def gen_rand_custom_contrast_color(from_color):
    """Generate a random dark or light color for a custom contrast."""
    # Get light-dark tonality level of the provided color
    dark_level = color_dark_level(
        from_color["R"], from_color["G"], from_color["B"])
    # If it is a dark color
    if dark_level >= 1:
        # from_color -> (255 - 384) -> (85 - 128)
        color = gen_rand_color(148, 255)
        # For high dark
        if dark_level == 3:
            # from_color -> (0 - 128) -> (0 - 42)
            color = gen_rand_color(62, 255)
    # If it is a light color
    elif dark_level <= -1:
        # from_color -> (384 - 640) -> (128 - 213)
        color = gen_rand_color(0, 108)
        # For high light
        if dark_level == -3:
            # from_color -> (640 - 765) -> (213 - 255)
            color = gen_rand_color(0, 193)
    return color
