from lfc_options import LFCOptions
from lfc_publisher import LFCPublisher
from lfc_rasterizer import LFCRasterizer

if __name__ == '__main__':
    options = LFCOptions()
    options.parse()

    rasterizer = LFCRasterizer()
    rasterizer.run(options)

    publisher = LFCPublisher()
    publisher.publish(rasterizer.glyphs, rasterizer.descent, options)
