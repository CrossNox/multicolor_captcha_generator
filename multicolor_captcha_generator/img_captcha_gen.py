from random import randint, choice
import pkg_resources
from PIL import Image
from .utils import (gen_rand_color, gen_rand_font,
                   gen_rand_size_font, gen_rand_color,
                   gen_rand_custom_contrast_color)
from .new_images import create_image_char
from .noise import (add_rand_circle_to_image, add_rand_ellipse_to_image,
                    add_rand_line_to_image, add_rand_noise_to_image,
                    add_rand_horizontal_line_to_image)
import logging
logger = logging.getLogger(__name__)


# Captcha 16:9 resolution sizes (captcha_size_num -> 0 to 12)
CAPTCHA_SIZE = [(256, 144), (426, 240), (640, 360), (768, 432),
                (800, 450), (848, 480),
                (960, 540), (1024, 576), (1152, 648), (1280, 720),
                (1366, 768), (1600, 900), (1920, 1080)]

# Font sizes range for each size
FONT_SIZE_RANGE = [(30, 45), (35, 80), (75, 125),
                   (80, 140), (85, 150), (90, 165), (100, 175),
                   (110, 185), (125, 195), (135, 210), (150, 230),
                   (165, 250), (180, 290)]

# Difficult levels captcha generation values (<lines in full img>, <circles in full img>)
DIFFICULT_LEVELS_VALUES = [(1, 10), (2, 17), (3, 25), (4, 50), (5, 70)]


class CaptchaGenerator:
    """
    Just an image captcha generator class.
    """
    def __init__(self, captcha_size_num=2):
        """Constructor"""
        # Limit provided captcha size num
        if captcha_size_num < 0:
            captcha_size_num = 0
        elif captcha_size_num >= len(CAPTCHA_SIZE):
            captcha_size_num = len(CAPTCHA_SIZE) - 1
        # Get captcha size
        self.captcha_size = CAPTCHA_SIZE[captcha_size_num]
        # Determine one char image height
        fourth_size = self.captcha_size[0] / 4
        if fourth_size - int(fourth_size) <= 0.5:
            fourth_size = int(fourth_size)
        else:
            fourth_size = int(fourth_size) + 1
        self.one_char_image_size = (fourth_size, fourth_size)
        # Determine font size according to image size
        font_size_min = FONT_SIZE_RANGE[captcha_size_num][0]
        font_size_max = FONT_SIZE_RANGE[captcha_size_num][1]
        self.font_size_range = (font_size_min, font_size_max)

    def images_join_horizontal(self, list_images):
        '''Horizontally join PIL images from list provided and create a single image from them.'''
        image = Image.new("RGB", (self.one_char_image_size[0]*len(list_images), \
                                  self.one_char_image_size[1]))
        x_offset = 0
        for img in list_images:
            image.paste(img, (x_offset, 0))
            x_offset += img.size[0]
        return image


    def gen_captcha_char_image(self, image_size, background_color=None, chars_mode="nums", add_noise=False):
        '''Generate an one-char image captcha. Image with a random positioned-rotated character.'''
        # If not background color provided, generate a random one
        if not background_color:
            background_color = gen_rand_color()
        # If invalid chars mode provided, use numbers
        chars_mode = chars_mode.lower()
        if chars_mode not in ("nums", "hex", "ascii"):
            chars_mode = "nums"
        # Generate a random character
        if chars_mode == "nums":
            character = str(randint(0, 9))
        elif chars_mode == "hex":
            characters_availables = "ABCDEF0123456789"
            character = choice(characters_availables)
        elif chars_mode == "ascii":
            characters_availables = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            character = choice(characters_availables)
        rand_color = gen_rand_custom_contrast_color(background_color)
        character_color = rand_color["color"]
        character_pos = (int(image_size[0]/4), randint(0, int(image_size[0]/4)))
        # Pick a random font with a random size, from the provided list
        rand_font_path = gen_rand_font()
        character_font = gen_rand_size_font(rand_font_path, self.font_size_range[0],
                                                 self.font_size_range[1])
        # Create an image of specified size, background color and character
        image = create_image_char(image_size, background_color["color"], character,
                                    character_color, character_pos, character_font)
        # Random rotate the created image between -55º and +55º
        image = image.rotate(randint(-55, 55), fillcolor=background_color["color"])
        # Add some random lines to image
        for _ in range(0, 2):
            add_rand_line_to_image(image, 3, character_color)
        # Add noise pixels to the image
        if add_noise:
            add_rand_noise_to_image(image, 200)
        # Return the generated image
        generated_captcha = {"image": image, "character": character}
        return generated_captcha


    def gen_captcha_image(self, difficult_level=2, chars_mode="nums", multicolor=False, \
            margin=True):
        '''Generate an image captcha.'''
        # Limit difficult level argument if out of expected range
        if difficult_level < 1:
            logger.info("Captcha generation for a lower difficult level than expected. Using difficult level 1.")
            difficult_level = 1
        elif difficult_level > 5:
            logger.info("Captcha generation for a higher difficult level than expected. Using difficult level 5.")
            difficult_level = 5
        # Set difficult level to array index values (1-5 to 0-4)
        difficult_level -= 1
        # Generate a RGB background color if the multicolor is disabled
        if not multicolor:
            image_background = gen_rand_color()
        # Generate 4 one-character images with a random char color in contrast to the generated 
        # background, a random font and font size, and random position-rotation
        one_char_images = []
        image_characters = ""
        for _ in range(0, 4):
            # Generate a RGB background color for each iteration if multicolor enabled
            if multicolor:
                image_background = gen_rand_color()
            # Generate a random character, a random character color in contrast to background 
            # and a random position for it
            captcha = self.gen_captcha_char_image(self.one_char_image_size, image_background, \
                    chars_mode)
            image = captcha["image"]
            image_characters = image_characters + captcha["character"]
            # Add the generated image to the list
            one_char_images.append(image)
        # Join the 4 characters images into one
        image = self.images_join_horizontal(one_char_images)
        # Add one horizontal random line to full image
        for _ in range(0, DIFFICULT_LEVELS_VALUES[difficult_level][0]):
            add_rand_horizontal_line_to_image(image, randint(1, 5))
        # Add some random circles to the image
        for _ in range(0, DIFFICULT_LEVELS_VALUES[difficult_level][1]):
            add_rand_circle_to_image(image, int(0.05*self.one_char_image_size[0]), \
                                          int(0.15*self.one_char_image_size[1]))
        # Add horizontal margins
        if margin:
            new_image = Image.new('RGBA', self.captcha_size, "rgb(0, 0, 0)")
            new_image.paste(image, (0, int((self.captcha_size[1]/2) - (image.height/2))))
            image = new_image
        # Return generated image captcha
        generated_captcha = {"image": image, "characters": image_characters}
        return generated_captcha
