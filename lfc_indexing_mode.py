"""Module that defines the indexing mode of the glyphs in a Lumina supported font"""

from enum import Enum

class IndexingMode(Enum):
    """Enum that defines the indexing mode of the glyphs in a Lumina supported font"""
    ASCII = 1
    UNICODE = 2

    def __str__(self):
        return 'ASCII' if self == IndexingMode.ASCII else 'UNICODE'
