import freetype
from lfc_glyph import LFCGlyph
from lfc_options import LFCOptions

class LFCRasterizer:
    def __init__(self) -> None:
        self.glyphs = []


    def run(self, options: LFCOptions) -> None:
        bitmap_index = 0

        for path, size, characters, _ in options.fonts:
            face = freetype.Face(path)
            face.set_pixel_sizes(0, size)

            for codepoint in characters:
                face.load_char(codepoint)

                glyph = LFCGlyph(
                    codepoint,
                    options.bpp,
                    bitmap_index,
                    (face.glyph.metrics.horiBearingY - face.glyph.metrics.height) // 64,
                    face
                )

                bitmap_index += len(glyph.data)

                self.glyphs.append(glyph)
