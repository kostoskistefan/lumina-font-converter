"""Module for converting a font file to a Lumina supported C file format"""

from lfc_options import LFCOptions
from lfc_rasterizer import LFCRasterizer
from lfc_indexer import LFCIndexer
from lfc_publisher import LFCPublisher

if __name__ == '__main__':
    options = LFCOptions()

    rasterizer = LFCRasterizer()
    rasterizer.rasterize(options)

    indexer = LFCIndexer()
    indexer.index(rasterizer.glyphs)

    publisher = LFCPublisher()
    publisher.publish(options, rasterizer.glyphs, indexer.indexing_mode, indexer.indices)
