import math
import freetype

class LFCGlyph:
    def __init__(self, codepoint: int, bpp: int, bitmap_index: int, y_bearing: int, face: freetype.Face) -> None:
        self.face = face
        self.bpp = bpp
        self.data = []
        self.width = face.glyph.bitmap.width
        self.height = face.glyph.bitmap.rows
        self.y_bearing = y_bearing
        self.codepoint = codepoint
        self.bitmap_index = bitmap_index

        # Calculate the actual advance as defined by the font
        actual_advance = (face.glyph.advance.x - face.glyph.metrics.horiBearingX) / 64

        # The space character only stores the actual advance, everything else is 0
        if codepoint == 32:
            self.advance = int(actual_advance)
            return

        # Adjust the advance since kerning is not supported.
        self.advance = max(self.width + 1, int(actual_advance - (math.fabs(self.width - actual_advance) / 2)))

        self.pixels_per_byte = 8 // bpp

        self.data = [0] * math.ceil(face.glyph.bitmap.rows * self.width / self.pixels_per_byte)

        # Pack and store the data
        for i in range(len(self.data)):
            for j in range(self.pixels_per_byte):
                if (i * self.pixels_per_byte + j) >= len(face.glyph.bitmap.buffer):
                    break

                pixel = face.glyph.bitmap.buffer[i * self.pixels_per_byte + j] >> (8 - bpp)
                self.data[i] |= pixel << ((self.pixels_per_byte - j - 1) * bpp)

        # Trim empty rows and columns and repack the data
        self.trim_and_repack_data()


    def trim_and_repack_data(self) -> None:
        bit_stream = ''

        # Convert data to a bit stream string
        for byte in self.data:
            bit_stream += f'{byte:08b}'

        # Trim leading zero rows
        while bit_stream.startswith('0' * (self.width * self.bpp)):
            bit_stream = bit_stream[self.width * self.bpp:]
            self.height -= 1

        # Trim trailing zero rows
        while bit_stream.endswith('0' * (self.width * self.bpp)):
            bit_stream = bit_stream[:-self.width * self.bpp]
            self.height -= 1
            self.y_bearing += 1

        # Split the bit stream into rows
        row_bit_width = self.width * self.bpp
        split_bit_stream = [bit_stream[i:i+row_bit_width] for i in range(0, len(bit_stream), row_bit_width)]

        # Trim leading zero columns
        while all(s.startswith('0' * self.bpp) for s in split_bit_stream):
            split_bit_stream = [s[self.bpp:] for s in split_bit_stream]
            self.width -= 1
            self.advance -= 1

        # Trim trailing zero columns
        while all(s.endswith('0' * self.bpp) for s in split_bit_stream):
            split_bit_stream = [s[:-self.bpp] for s in split_bit_stream]
            self.width -= 1
            self.advance -= 1

        # Repack the bit stream
        bit_stream = ''.join(split_bit_stream)

        # Split the bit stream into string bytes
        byte_data = [bit_stream[i:i+8] for i in range(0, len(bit_stream), 8)]

        # Pad the last byte with zeros
        byte_data[-1] = byte_data[-1] + '0' * (8 - len(byte_data[-1])) 

        # Convert the string bytes to integers
        self.data = list(map(lambda x: int(x, 2), byte_data))


    def publish_bitmap(self) -> str:
        output = f'    // Codepoint: {f"0x{self.codepoint:0X}" if self.codepoint >= 128 else self.codepoint}\n    '

        column = 0

        for byte in self.data:
            output += f'0x{byte:02x}, '

            column += self.pixels_per_byte

            if column >= self.width:
                column = 0
                output += '\n    '

        return output


    def publish_metadata(self) -> str:
        output = '    { '
        output += f'.bitmap_index = {self.bitmap_index}, '
        output += f'.width = {self.width}, '
        output += f'.height = {self.height}, '
        output += f'.advance = {self.advance}, '
        output += f'.y_bearing = {self.y_bearing}'
        output += f' }}, // Codepoint: {f"0x{self.codepoint:0X}" if self.codepoint >= 128 else self.codepoint}'

        return output


    def __str__(self) -> str:
        output = ''

        output += f'Codepoint: {self.codepoint}\n'
        output += f'Width: {self.width}\n'
        output += f'Height: {self.height}\n'
        output += f'Advance: {self.advance}\n'
        output += f'Y bearing: {self.y_bearing}\n'
        output += f'Bitmap index: {self.bitmap_index}\n'

        column = 0

        output += '\nPacked data:\n'

        for byte in self.data:
            output += f'{byte:02x} '

            column += self.pixels_per_byte

            if column >= self.width:
                column = 0
                output += '\n'

        if 0 < column < self.width:
            output += '\n'

        row = 0
        column = 0

        output += '\nUnpacked data:\n'

        for byte in self.data:
            for j in reversed(range(self.pixels_per_byte)):
                pixel = (byte >> (j * self.bpp)) & ((1 << self.bpp) - 1)

                if self.bpp == 8:
                    output += ' . ' if pixel == 0 else f'{pixel:02x} '
                else:
                    output += '. ' if pixel == 0 else f'{pixel:01x} '

                column += 1

                if column == self.width:
                    row += 1
                    column = 0
                    output += '\n'

                if row == self.height:
                    break

        output += '\n'

        return output
