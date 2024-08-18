"""Module for rasterizing font characters into Lumina supported glyphs"""

import math
import freetype
from lfc_glyph import LFCGlyph

class LFCRasterizer:
    """Class for rasterizing font characters into Lumina supported glyphs"""
    def __init__(self):
        self.glyphs = []


    def rasterize(self, options):
        """Function that rasterizes the font characters into Lumina supported glyphs"""
        # Calculate the max ascent
        max_ascent = self.calculate_max_ascent(options)

        # Iterate over all fonts and rasterize them
        self.rasterize_font(max_ascent, options)


    def calculate_max_ascent(self, options):
        """Function that calculates the maximum ascent of the font"""
        # Find the character with the highest bitmap_top (ascent)
        face = freetype.Face(options.font)
        face.set_char_size(options.height << 6)

        max_ascent = 0

        for character in options.characters:
            # Load the character from the font
            face.load_char(character, freetype.FT_LOAD_FLAGS['FT_LOAD_BITMAP_METRICS_ONLY'])

            # Update the max ascent
            max_ascent = max(max_ascent, face.glyph.bitmap_top)

        return max_ascent


    def rasterize_font(self, max_ascent, options):
        """Function that rasterizes the font into glyphs"""
        # Load the font face
        face = freetype.Face(options.font)

        # Set the character size
        face.set_char_size(options.height << 6)

        character_data_index = 0

        glyph_bpp_map_divisor = 1 << (8 - options.bpp)

        pixels_per_byte = 8 // options.bpp

        # Iterate over all requested characters
        for character in options.characters:
            # Load the character from the font
            face.load_char(character)

            # Create the glyph object
            glyph = LFCGlyph(
                options.bpp,
                character,
                face.glyph.bitmap.width,
                face.glyph.bitmap.rows,
                face.glyph.advance.x >> 6,
                max_ascent - face.glyph.bitmap_top,
                character_data_index,
                list(map(lambda x: x // glyph_bpp_map_divisor, face.glyph.bitmap.buffer))
            )

            if any(face.glyph.bitmap.buffer):
                # Trim leading and trailing zero rows from the glyph data
                glyph.trim_zero_axes()

                # Adjust the bitmap width of the glyph to a multiple of bpp
                glyph.adjust_bitmap_width()

            # Update the character data index for the next character
            character_data_index += math.ceil(glyph.width / pixels_per_byte) * glyph.height

            # Add the glyph to the list
            self.glyphs.append(glyph)
