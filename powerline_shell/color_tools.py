from colorsys import rgb_to_hls
# md5 deprecated since Python 2.5
try:
    from md5 import md5
except ImportError:
    from hashlib import md5
import sys

from .utils import py3


def rgb_string_to_tuple(string):
    if len(string) != 6:
        raise ValueError(
            'only six-character colors are supported (got {})'.format(string))

    return tuple(int(hex, 16) for hex in (string[:2], string[2:4], string[4:]))


def get_contrasting_color(rgb):
    r, g, b = tuple(c / 255.0 for c in rgb)
    h, l, s = rgb_to_hls(r, g, b)

    return (0, 0, 0) if l > 0.5 else (255, 255, 255)


def get_random_color_and_contrast(string):
    encoded_string = string.encode('utf-8') if py3 else string
    hashed_string = md5(encoded_string).hexdigest()[:6]
    random_color = rgb_string_to_tuple(hashed_string)
    contrast_color = get_contrasting_color(random_color)

    return random_color, contrast_color
