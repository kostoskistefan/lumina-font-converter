from lfc_options import *
from lfc_rasterizer import *
from lfc_indexer import *
from lfc_publisher import *

if __name__ == '__main__':
    options = LFCOptions()

    rasterizer = LFCRasterizer()
    rasterizer.rasterize(options)

    indexer = LFCIndexer()
    indexer.index(rasterizer.glyphs, options.bpp)

    publisher = LFCPublisher()
    publisher.publish(options, rasterizer.glyphs, indexer.indexing_mode, indexer.indices)
