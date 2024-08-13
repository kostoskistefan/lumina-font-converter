"""Module for storing and optimizing a glyph in a Lumina supported font"""

import math

class LFCGlyph:
    """Class representing a glyph in a Lumina supported font"""

    def __init__(self, bpp, code, width, height, advance, y_offset, bitmap_index, data):
        self.bpp = bpp
        self.data = data
        self.code = code
        self.width = width
        self.height = height
        self.advance = advance
        self.y_offset = y_offset
        self.bitmap_index = bitmap_index


    def trim_zero_axes(self):
        """Function that trims unnecessary leading/trailing zero rows/columns from the glyph data"""
        self._trim_leading_zero_rows()
        self._trim_trailing_zero_rows()
        self._trim_leading_zero_columns()
        self._trim_trailing_zero_columns()


    def adjust_width(self):
        """Function that adjusts the glyph's width to a multiple of bpp"""
        # Calculate the pixels per byte
        pixels_per_byte = 8 // self.bpp

        # Calculate the amount of padding needed to make the width a multiple of bpp
        column_padding = math.ceil(self.width / pixels_per_byte) * pixels_per_byte - self.width

        # Add padding
        for row in range(self.height):
            index = row * (self.width + column_padding) + self.width
            self.data[index:index] = [0] * column_padding

        # Update the glyph's data and width
        self.width += column_padding


    def trim_non_qualifying_rows(self, percentage):
        """Function that trims the glyph's rows based on the given percentage"""
        # Calculate the max value a row can have based on the bpp
        max_row_value = sum([2 ** (self.bpp - 1)] * self.width)

        for row in range(self.height):
            # Calculate the sum of the values of the current row
            row_sum = sum(self.data[row * self.width : row * self.width + self.width])

            # If the sum is less than a given percentage of the max value, remove the row
            if row_sum / max_row_value < percentage:
                self.height -= 1
                del self.data[row * self.width : row * self.width + self.width]


    def _trim_leading_zero_columns(self):
        zero_column_count = 0

        # Count leading zero columns
        for column in range(self.width):
            if all(self.data[row * self.width + column] == 0 for row in range(self.height)):
                zero_column_count += 1
            else:
                break

        # Remove zero columns and adjust the glyph's width
        for _ in range(zero_column_count):
            self.width -= 1

            for row in range(self.height):
                self.data.pop(row * (self.width - zero_column_count + 1))


    def _trim_trailing_zero_columns(self):
        zero_column_count = 0

        # Count leading zero columns
        for column in range(self.width - 1, -1, -1):
            if all(self.data[row * self.width + column] == 0 for row in range(self.height)):
                zero_column_count += 1
            else:
                break

        # Remove zero columns and adjust the glyph's width
        for _ in range(zero_column_count):
            self.width -= 1

            for row in range(self.height):
                self.data.pop(row * (self.width - zero_column_count + 1) + self.width)


    def _trim_leading_zero_rows(self):
        zero_row_count = 0

        # Count leading zero rows
        for row in range(0, len(self.data), self.width):
            if not any(self.data[row : row + self.width]):
                zero_row_count += 1
            else:
                break

        # Adjust the glyph based on the number of leading zero rows
        self.data = self.data[zero_row_count * self.width:]
        self.height -= zero_row_count
        self.y_offset += zero_row_count


    def _trim_trailing_zero_rows(self):
        zero_row_count = 0

        # Count trailing zero rows
        for row in range(len(self.data) - 1, self.width, -self.width):
            if not any(self.data[row - self.width : row]):
                zero_row_count += 1
            else:
                break

        # Adjust the glyph based on the number of trailing zero rows
        self.data = self.data[:len(self.data) - zero_row_count * self.width]
        self.height -= zero_row_count


    def __str__(self):
        output = ''

        # Print the glyph information
        output += f'bpp: {self.bpp}\n'
        output += f'code: {self.code}\n'
        output += f'width: {self.width}\n'
        output += f'height: {self.height}\n'
        output += f'advance: {self.advance}\n'
        output += f'y_offset: {self.y_offset}\n'
        output += f'bitmap_index: {self.bitmap_index}\n'

        output += '\nraw data:\n'

        raw_data_padding = len(str(1 << self.bpp))

        # Print the bitmap as binary
        for j in range(self.height):
            for i in range(self.width):
                output += f'{self.data[j * self.width + i]:0{raw_data_padding}d} '
            output += '\n'

        output += '\nASCII art:\n'

        # Print the bitmap as ascii art
        ascii_art_intensity_characters = ' .-=+*#@'

        for j in range(self.height):
            for i in range(self.width):
                character_data = self.data[j * self.width + i]
                if self.bpp == 1:
                    output += ascii_art_intensity_characters[character_data * 7]
                elif self.bpp == 2:
                    output += ascii_art_intensity_characters[character_data * 2]
                elif self.bpp == 4:
                    output += ascii_art_intensity_characters[character_data // 2]
                elif self.bpp == 8:
                    output += ascii_art_intensity_characters[character_data // 32]
            output += '\n'

        return output
