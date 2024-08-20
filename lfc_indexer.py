"""Module for indexing glyphs in a Lumina supported font"""

from lfc_indexing_mode import IndexingMode

class LFCIndexer:
    """Class for indexing glyphs in a Lumina supported font"""

    def __init__(self):
        self.indices = []
        self.indexing_mode = IndexingMode.ASCII


    def detect_indexing_mode(self, glyphs):
        """Function that detects the indexing mode of the glyphs"""
        # Check if all glyphs fall into the ASCII range
        if all(g.code >= 32 and g.code <= 126 for g in glyphs):
            return IndexingMode.ASCII

        return IndexingMode.UNICODE


    def index(self, glyphs):
        """Function that indexes the glyphs based on the detected indexing mode"""
        self.indexing_mode = self.detect_indexing_mode(glyphs)

        match self.indexing_mode:
            case IndexingMode.ASCII:
                # Create an index list with a length of the value of the highest glyph code
                self.indices = [0] * (max(glyph.code for glyph in glyphs) - glyphs[0].code + 1)

                for (index, glyph) in enumerate(glyphs):
                    self.indices[glyph.code - glyphs[0].code] = index + 1

            case IndexingMode.UNICODE:
                # Create an index list with a length of the number of glyphs
                self.indices = list(range(1, len(glyphs) + 1))
