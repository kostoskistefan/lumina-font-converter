import freetype
from lfc_glyph import * 
from lfc_constants import LFC_BITMAP_ROW_QUALIFICATION_THRESHOLD

class LFCRasterizer:
    def __init__(self):
        self.glyphs = []


    def rasterize(self, options):
        # Calculate the max ascent
        max_ascent = self.calculate_max_ascent(options)

        # Iterate over all fonts and rasterize them
        self.rasterize_font(max_ascent, options)


    def calculate_max_ascent(self, options):
        # Find the character with the highest bitmap_top (ascent)
        face = freetype.Face(options.font)
        face.set_char_size(options.height << 6)

        max_ascent = 0

        for character in options.characters:
            # Load the character from the font
            face.load_char(character, freetype.FT_LOAD_BITMAP_METRICS_ONLY)

            # Update the max ascent
            if face.glyph.bitmap_top > max_ascent:
                max_ascent = face.glyph.bitmap_top

        return max_ascent


    def rasterize_font(self, max_ascent, options):
        # Load the font face
        face = freetype.Face(options.font)

        # Set the character size
        face.set_char_size(options.height << 6)

        character_data_index = 0

        glyph_bpp_map_divisor = 1 << (8 - options.bpp)

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

                # Adjust the width of the glyph to make it divisible by 8
                glyph.adjust_width()

                # Trim rows that contribute less than a certain percentage of the maximum value that a row can have
                # Ex. if the max summed pixel values per row are 128, and a row only has 1 very dim pixel set 
                # (for example: a brightness value of 5), and the percentage is set to 5%, the row will be removed. 
                # This reduces the memory footprint of the generated font, for use in MCUs with limited memory
                glyph.trim_non_qualifying_rows(LFC_BITMAP_ROW_QUALIFICATION_THRESHOLD)

            # Update the character data index for the next character
            character_data_index += len(glyph.data)

            # Add the glyph to the list
            self.glyphs.append(glyph)
