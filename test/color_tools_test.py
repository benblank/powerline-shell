import hashlib
import mock
from parameterized import parameterized
import unittest

import powerline_shell  # for mocking; see GetRandomColorAndContrast.test_works
from powerline_shell.color_tools import *


def generate_sample_colors():
    """Generate a sampling of colors across the RGB space.

    This generates the product of 16 possible values for each channel, for a
    total of 4,096 sample colors.
    """
    return [(r, g, b) for r in range(0, 256, 17)
            for g in range(0, 256, 17) for b in range(0, 256, 17)]


def get_sample_colors():
    """Get the sample colors in a format suitable for using with
    `parameterized.expand`.
    """

    return [(str(color), color) for color in generate_sample_colors()]


def get_sample_colors_with_hex():
    """Get the sample colors, plus their lower- and uppercase hexadecimal
    representations, in a format suitable for use with `parameterized.expand`.
    """

    tuples = generate_sample_colors()
    lower = ['{0:02x}{1:02x}{2:02x}'.format(r, g, b) for (r, g, b) in tuples]
    upper = [color.upper() for color in lower]

    return ((str(tuples[i]), tuples[i], lower[i], upper[i]) for i in range(len(tuples)))


def get_luminosity(color):
    """Get the lumiunosity value for a color.

    Colors are expected to be a sequence of three integers in the range 0-255.
    Luminosity is calculated in the same fashion as does the `colorsys` module.
    """

    r, g, b = (c / 255.0 for c in color)

    return (min(r, g, b) + max(r, g, b)) / 2.0


class RgbStringToTupleTestCase(unittest.TestCase):
    def test_short_strings_raise(self):
        self.assertRaises(ValueError, rgb_string_to_tuple, '')
        self.assertRaises(ValueError, rgb_string_to_tuple, '1')
        self.assertRaises(ValueError, rgb_string_to_tuple, '12')
        self.assertRaises(ValueError, rgb_string_to_tuple, '123')
        self.assertRaises(ValueError, rgb_string_to_tuple, '1234')
        self.assertRaises(ValueError, rgb_string_to_tuple, '12345')

    def test_long_strings_raise(self):
        self.assertRaises(ValueError, rgb_string_to_tuple, '1234567')
        self.assertRaises(ValueError, rgb_string_to_tuple, '12345678')
        self.assertRaises(ValueError, rgb_string_to_tuple, '123456789')
        self.assertRaises(ValueError, rgb_string_to_tuple, '1234567890')

    def test_non_hex_characters_raise(self):
        self.assertRaises(ValueError, rgb_string_to_tuple, '00000g')
        self.assertRaises(ValueError, rgb_string_to_tuple, '0000g0')
        self.assertRaises(ValueError, rgb_string_to_tuple, '000g00')
        self.assertRaises(ValueError, rgb_string_to_tuple, '00g000')
        self.assertRaises(ValueError, rgb_string_to_tuple, '0g0000')
        self.assertRaises(ValueError, rgb_string_to_tuple, 'g00000')
        self.assertRaises(ValueError, rgb_string_to_tuple, '!@#$%^')

    @parameterized.expand(get_sample_colors_with_hex)
    def test_works(self, _, color, lower, upper):
        self.assertEqual(color, rgb_string_to_tuple(lower))
        self.assertEqual(color, rgb_string_to_tuple(upper))


class GetContrastingColorTestCase(unittest.TestCase):
    def test_too_few_channels_raises(self):
        self.assertRaises(ValueError, get_contrasting_color, ())
        self.assertRaises(ValueError, get_contrasting_color, (1, ))
        self.assertRaises(ValueError, get_contrasting_color, (1, 2))

    def test_too_many_channels_raises(self):
        self.assertRaises(ValueError, get_contrasting_color, (1, 2, 3, 4))
        self.assertRaises(ValueError, get_contrasting_color, (1, 2, 3, 4, 5))

    @parameterized.expand(get_sample_colors)
    def test_works(self, _, color):
        luminosity = get_luminosity(color)
        expected = (0, 0, 0) if luminosity > 0.5 else (255, 255, 255)

        self.assertEqual(expected, get_contrasting_color(color))


class GetRandomColorAndContrast(unittest.TestCase):
    """`get_random_color_and_contrast` isn't as exhaustively tested as the
    above functions, as it is primarily a composition of them.
    """

    @mock.patch('powerline_shell.color_tools.md5')
    def test_works(self, mock_md5):
        mock_md5.return_value.hexdigest.return_value.__getitem__.return_value = '012345'
        self.assertEqual(((1, 35, 69), (255, 255, 255)),
                         get_random_color_and_contrast(''))

        mock_md5.return_value.hexdigest.return_value.__getitem__.return_value = 'abcdef'
        self.assertEqual(((171, 205, 239), (0, 0, 0)),
                         get_random_color_and_contrast(''))
