from random import randint
from PIL import ImageDraw


def add_rand_circle_to_image(image, min_size, max_size, circle_color="notSet"):
    '''Draw a random circle to a PIL image.'''
    x = randint(0, image.width)
    y = randint(0, image.height)
    rad = randint(min_size, max_size)
    if circle_color == "notSet":
        circle_color = "rgb({}, {}, {})".format(str(randint(0, 255)),
                                                str(randint(0, 255)),
                                                str(randint(0, 255)))
    draw = ImageDraw.Draw(image)
    draw.ellipse((x, y, x + rad, y + rad),
                 fill=circle_color or "notSet", outline=circle_color)


def add_rand_ellipse_to_image(image, w_min, w_max, h_min, h_max, ellipse_color="notSet"):
    '''Draw a random ellipse to a PIL image.'''
    x = randint(0, image.width)
    y = randint(0, image.height)
    w = randint(w_min, w_max)
    h = randint(h_min, h_max)
    if ellipse_color == "notSet":
        ellipse_color = "rgb({}, {}, {})".format(str(randint(0, 255)),
                                                 str(randint(0, 255)),
                                                 str(randint(0, 255)))
    draw = ImageDraw.Draw(image)
    draw.ellipse((x, y, x + w, y + h), fill=ellipse_color,
                 outline=ellipse_color)


def add_rand_line_to_image(image, line_width=5, line_color="notSet"):
    '''Draw a random line to a PIL image.'''
    # Get line random start position
    line_x0 = randint(0, image.width)
    line_y0 = randint(0, image.height)
    # If line x0 is in center-to-right
    if line_x0 >= image.width / 2:
        # Line x1 from 0 to line_x0 position - 20% of image width
        line_x1 = randint(0, line_x0 - int(0.2 * image.width))
    else:
        # Line x1 from line_x0 position + 20% of image width to max image width
        line_x1 = randint(line_x0 + int(0.2 * image.width), image.width)
    # If line y0 is in center-to-bottom
    if line_y0 >= image.height / 2:
        # Line y1 from 0 to line_y0 position - 20% of image height
        line_y1 = randint(0, line_y0 - int(0.2 * image.height))
    else:
        # Line y1 from line_y0 position + 20% of image height to max image height
        line_y1 = randint(line_y0 + int(0.2 * image.height), image.height)
    # Generate a rand line color if not provided
    if line_color == "notSet":
        line_color = "rgb({}, {}, {})".format(str(randint(0, 255)),
                                              str(randint(0, 255)),
                                              str(randint(0, 255))
                                              )
    # Get image draw interface and draw the line on it
    draw = ImageDraw.Draw(image)
    draw.line((line_x0, line_y0, line_x1, line_y1),
              fill=line_color, width=line_width)


def add_rand_noise_to_image(image, num_pixels):
    '''Add noise pixels to a PIL image.'''
    draw = ImageDraw.Draw(image)
    for _ in range(0, num_pixels):
        pixel_color = "rgb({}, {}, {})".format(str(randint(0, 255)),
                                               str(randint(0, 255)),
                                               str(randint(0, 255))
                                               )
        draw.point((randint(0, image.width), randint(
            0, image.height)), pixel_color)


def add_rand_horizontal_line_to_image(image, line_width=5, line_color="notSet"):
    '''Draw a random line to a PIL image.'''
    # Get line random start position (x between 0 and 20% image width; y with full height range)
    x0 = randint(0, int(0.2 * image.width))
    y0 = randint(0, image.height)
    # Get line end position (x1 symetric to x0; y random from y0 to image height)
    x1 = image.width - x0
    y1 = randint(y0, image.height)
    # Generate a rand line color if not provided
    if line_color == "notSet":
        line_color = "rgb({}, {}, {})".format(str(randint(0, 255)),
                                              str(randint(0, 255)),
                                              str(randint(0, 255))
                                              )
    # Get image draw interface and draw the line on it
    draw = ImageDraw.Draw(image)
    draw.line((x0, y0, x1, y1), fill=line_color, width=5)
