import freetype
from lfc_glyph import LFCGlyph
from lfc_options import LFCOptions

class LFCRasterizer:
    def __init__(self) -> None:
        self.glyphs = []
        self.descent = 0


    def run(self, options: LFCOptions) -> None:
        bitmap_index = 0

        for path, size, characters, _ in options.fonts:
            face = freetype.Face(path)
            face.set_pixel_sizes(0, size)

            max_descent = 0  # Variable to track the maximum descent (lowest point)
            max_ascent = 0   # Variable to track the maximum ascent (highest point)

            for codepoint in characters:
                face.load_char(codepoint)

                glyph = LFCGlyph(
                    codepoint,
                    options.bpp,
                    bitmap_index,
                    face.glyph.metrics.horiBearingY // 64,
                    face
                )

                bitmap_index += len(glyph.data)

                self.glyphs.append(glyph)
    
        max_height = max(glyph.height for glyph in self.glyphs)
        max_y_bearing = max(glyph.y_bearing for glyph in self.glyphs)

        self.descent = max_height - max_y_bearing
