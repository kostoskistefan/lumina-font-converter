"""Module that generates the header and source files for the Lumina supported font converter"""

import os
import sys
import datetime
import textwrap
from lfc_constants import LFC_VERSION, LFC_PUBLISHER_INDENTATION
from lfc_indexing_mode import IndexingMode

class LFCPublisher:
    """Class that generates the header and source files for the Lumina supported font converter"""
    def __init__(self):
        pass


    def publish(self, options, glyphs, indexing_mode, indices):
        """Function that generates the Lumina compatible font files"""
        output_directory = self.create_output_directory()

        header_file_content = self.generate_header_file(options, glyphs, indexing_mode)
        source_file_content = self.generate_source_file(options, glyphs, indexing_mode, indices)

        header_file_path = os.path.join(output_directory, f'{options.name}.h')
        source_file_path = os.path.join(output_directory, f'{options.name}.c')

        with open(header_file_path, 'w', encoding='utf-8') as header_file:
            header_file.write(header_file_content)

        with open(source_file_path, 'w', encoding='utf-8') as source_file:
            source_file.write(source_file_content)


    def indent(self, string):
        """Function that adds indentation to a given string"""
        return f'{LFC_PUBLISHER_INDENTATION}{string}'


    def create_output_directory(self):
        """Function that creates the output directory"""
        output_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        return output_path


    def generate_header_file(self, options, glyphs, indexing_mode):
        """Function that generates the header file content"""
        output = '#pragma once\n\n'
        output += self.generate_info(options)

        if indexing_mode == IndexingMode.UNICODE:
            for (index, glyph) in enumerate(glyphs):
                output += f'#define LUMINA_FONT_GLYPH_{glyph.code:X} {index}\n'
            output += '\n'

        output += f'extern const lumina_font_t {options.name}_font;'

        return output


    def generate_source_file(self, options, glyphs, indexing_mode, indices):
        """Function that generates the source file content"""
        output = '#include "lumina_font.h"\n'
        output += f'#include "{options.name}.h"\n\n'
        output += self.generate_info(options)
        output += self.generate_glyphs_bitmap(options.name, glyphs, options.bpp)
        output += self.generate_glyphs_metadata(options.name, glyphs)
        output += self.generate_glyphs_lookup_table(options.name, indices, glyphs)
        output += self.generate_font(options, glyphs, indexing_mode)

        return output


    def generate_info(self, options):
        """Function that generates the font information"""
        command = textwrap.fill(
                ' '.join(sys.argv),
                width=110,
                initial_indent='',
                subsequent_indent="//          ")

        output = f'// {"-" * 120}\n'
        output += f'// Font name: {options.name}\n'
        output += f'// Font height: {options.height}px\n'
        output += f'// Font bpp: {options.bpp}\n'
        output += f'// Font file: {os.path.basename(options.font)}\n//\n'
        output += f'// Generated with Lumina Font Converter v{LFC_VERSION}\n'
        output += '// https://github.com/kostoskistefan/lumina-font-converter\n'
        output += f'// Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
        output += f'// Command: {command}\n'
        output += f'// {"-" * 120}\n\n'

        return output


    def generate_glyphs_bitmap(self, font_name, glyphs, bpp):
        """Function that generates the glyph bitmap data"""
        output = f'static const uint8_t {font_name}_glyph_bitmap[] = {{\n'

        for (index, glyph) in enumerate(glyphs):
            output += (
                    self.indent('// ') +
                    f'Code: {glyph.code:{"d" if glyph.code < 128 else "x"}}, '
                    f'Width: {glyph.width}, '
                    f'Height: {glyph.height}\n'
            )

            glyph_bitstream = ''.join([f'{chunk:0{bpp}b}' for chunk in glyph.data])

            columns = 0

            output += self.indent('')

            for i in range(0, len(glyph_bitstream), 8):
                output += f'0x{int(glyph_bitstream[i:i+8], 2):0>02x}, '

                columns += 8

                if columns >= glyph.width * bpp:
                    columns = 0
                    output += '\n'

                    if i < len(glyph_bitstream) - 8:
                        output += self.indent('')

            if index < len(glyphs) - 1:
                output += '\n'

        output += '};\n\n'

        return output


    def generate_glyphs_metadata(self, font_name, glyphs):
        """Function that generates the glyph metadata"""
        output = f'static const lumina_font_glyph_metadata_t {font_name}_glyph_metadata[] = {{\n'

        max_width_digits = max(len(str(glyph.width)) for glyph in glyphs)
        max_height_digits = max(len(str(glyph.height)) for glyph in glyphs)
        max_advance_digits = max(len(str(glyph.advance)) for glyph in glyphs)
        max_y_offset_digits = max(len(str(glyph.y_offset)) for glyph in glyphs)
        max_bitmap_index_digits = max(len(str(glyph.bitmap_index)) for glyph in glyphs)

        for glyph in glyphs:
            output += self.indent('{ ')
            output += f'.width = {glyph.width:{max_width_digits}}, '
            output += f'.height = {glyph.height:{max_height_digits}}, '
            output += f'.advance = {glyph.advance:{max_advance_digits}}, '
            output += f'.y_offset = {glyph.y_offset:{max_y_offset_digits}}, '
            output += f'.bitmap_index = {glyph.bitmap_index:{max_bitmap_index_digits}} '
            output += f'}}, // Code: {glyph.code:{"d" if glyph.code < 128 else "x"}}\n'

        output += '};\n\n'

        return output


    def generate_glyphs_lookup_table(self, font_name, indices, glyphs):
        """Function that generates the glyph lookup table"""
        output = f'static const uint8_t {font_name}_glyph_lut[] = {{\n'

        for index in indices:
            output += self.indent(f'{index}, ')
            output += f'// Code: {glyphs[index].code:{"d" if glyphs[index].code < 128 else "x"}}\n'

        output += '};\n\n'

        return output


    def generate_font(self, options, glyphs, indexing_mode):
        """Function that generates the C extern font struct"""
        output = f'const lumina_font_t {options.name}_font = {{\n'
        output += self.indent(f'.bpp = {options.bpp},\n')
        output += self.indent(f'.first_valid_index = {glyphs[0].code},\n')
        output += self.indent(f'.last_valid_index = {glyphs[-1].code},\n')
        output += self.indent(f'.glyph_lut = {options.name}_glyph_lut,\n')
        output += self.indent(f'.glyph_bitmap = {options.name}_glyph_bitmap,\n')
        output += self.indent(f'.glyph_metadata = {options.name}_glyph_metadata,\n')
        output += self.indent(f'.indexing_mode = LUMINA_FONT_INDEXING_MODE_{indexing_mode},\n')
        output += '};'

        return output
