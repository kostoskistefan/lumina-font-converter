from lfc_indexing_mode import *
from lfc_glyph import LFCGlyph

class LFCIndexer:
    def __init__(self):
        self.indices = []
        self.indexing_mode = IndexingMode.ASCII


    def detect_indexing_mode(self, glyphs):
        # Check if all glyphs fall into the ASCII range
        if all(g.code >= 32 and g.code <= 126 for g in glyphs):
            return IndexingMode.ASCII
        else:
            return IndexingMode.Unicode


    def index(self, glyphs, bpp):
        self.indexing_mode = self.detect_indexing_mode(glyphs)

        match self.indexing_mode:
            case IndexingMode.ASCII:
                # Create an index list with a length of the value of the highest glyph code
                self.indices = [-1] * (max([glyph.code for glyph in glyphs]) - glyphs[0].code + 1)

                for (index, glyph) in enumerate(glyphs):
                    self.indices[glyph.code - glyphs[0].code] = index

            case IndexingMode.Unicode:
                # Create an index list with a length of the number of glyphs 
                self.indices = list(range(len(glyphs)))
