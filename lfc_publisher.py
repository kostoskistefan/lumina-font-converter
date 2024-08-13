import os
import sys
import math 
import datetime
import textwrap
from lfc_constants import *
from lfc_indexing_mode import *

class LFCPublisher:
    def __init__(self):
        pass


    def publish(self, options, glyphs, indexing_mode, indices):
        # create_output_directory()

        header_file_content = self.generate_header_file(options, glyphs, indexing_mode)
        source_file_content = self.generate_source_file(options, glyphs, indexing_mode, indices)

        print(header_file_content)
        print(source_file_content)


    def create_output_directory(self):
        output_path = os.path.join(os.path.realpath(__file__), 'output')

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        return output_path


    def generate_header_file(self, options, glyphs, indexing_mode):
        output = '#pragma once\n\n'
        output += self.generate_info(options)

        if indexing_mode == IndexingMode.Unicode:
            for (index, glyph) in enumerate(glyphs):
                output += f'#define LUMINA_FONT_GLYPH_{glyph.code:X} {index}\n'

        output += f'extern const lumina_font_t {options.name}_font;'

        return output


    def generate_source_file(self, options, glyphs, indexing_mode, indices):
        output = f'#include "lumina_font.h"\n'
        output += f'#include "{options.name}.h"\n\n'
        output += self.generate_info(options)
        output += self.generate_glyphs_bitmap(options.name, glyphs, options.bpp)
        output += self.generate_glyphs_metadata(options.name, glyphs)
        output += self.generate_glyphs_lookup_table(options.name, indices)
        output += self.generate_font(options, glyphs, indexing_mode)

        return output


    def generate_info(self, options):
        command = textwrap.fill(' '.join(sys.argv), width=110, initial_indent='', subsequent_indent=f"//          ")

        output = f'// {"-" * 120}\n'
        output += f'// Font name: {options.name}\n'
        output += f'// Font height: {options.height}px\n'
        output += f'// Font bpp: {options.bpp}\n'
        output += f'// Font file: {os.path.basename(options.font)}\n//\n'
        output += f'// Generated with Lumina Font Converter v{LFC_VERSION}\n'
        output += f'// https://github.com/kostoskistefan/lumina-font-converter\n'
        output += f'// Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
        output += f'// Command: {command}\n'
        output += f'// {"-" * 120}\n\n'

        return output


    def generate_glyphs_bitmap(self, font_name, glyphs, bpp):
        output = f'static const uint8_t {font_name}_glyph_bitmap[] = {{\n'

        for (index, glyph) in enumerate(glyphs):
            output += f'{LFC_PUBLISHER_INDENTATION}// Code: {glyph.code}, Width: {glyph.width}, Height: {glyph.height}\n'

            glyph_bitstream = ''.join([f'{chunk:0{bpp}b}' for chunk in glyph.data])
            hex_glyph_data = [f'0x{int(glyph_bitstream[i:i+8], 2):0>02x}' for i in range(0, len(glyph_bitstream), 8)]

            columns = 0

            output += f'{LFC_PUBLISHER_INDENTATION}'

            for i in range(len(hex_glyph_data)):
                output += f'{hex_glyph_data[i]}, '

                columns += 8 

                if columns >= glyph.width * bpp:
                    output += f'\n{LFC_PUBLISHER_INDENTATION}'
                    columns = 0

            output += '\n'

            if index < len(glyphs) - 1:
                output += '\n'

        output += '};\n\n'

        return output


    def generate_glyphs_metadata(self, font_name, glyphs):
        output = f'static const lumina_font_glyph_metadata_t {font_name}_glyph_metadata[] = {{\n'

        max_width_digits = max(len(str(glyph.width)) for glyph in glyphs)
        max_height_digits = max(len(str(glyph.height)) for glyph in glyphs)
        max_advance_digits = max(len(str(glyph.advance)) for glyph in glyphs)
        max_y_offset_digits = max(len(str(glyph.y_offset)) for glyph in glyphs)
        max_bitmap_index_digits = max(len(str(glyph.bitmap_index)) for glyph in glyphs)

        for glyph in glyphs:
            output += f'{LFC_PUBLISHER_INDENTATION}'
            output += f'{{ '
            output += f'.width = {glyph.width:{max_width_digits}}, '
            output += f'.height = {glyph.height:{max_height_digits}}, '
            output += f'.advance = {glyph.advance:{max_advance_digits}}, '
            output += f'.y_offset = {glyph.y_offset:{max_y_offset_digits}}, '
            output += f'.bitmap_index = {glyph.bitmap_index:{max_bitmap_index_digits}} '
            output += f'}},\n'

        output += '};\n\n'

        return output


    def generate_glyphs_lookup_table(self, font_name, indices):
        output = f'static const uint8_t {font_name}_glyph_lut[] = {{\n'

        for index in indices:
            output += f'{LFC_PUBLISHER_INDENTATION}{index},\n'

        output += '};\n\n'

        return output


    def generate_font(self, options, glyphs, indexing_mode):
        output = f'const lumina_font_t {options.name}_font = {{\n'
        output += f'{LFC_PUBLISHER_INDENTATION}.bpp = {options.bpp},\n'
        output += f'{LFC_PUBLISHER_INDENTATION}.first_valid_index = {glyphs[0].code},\n'
        output += f'{LFC_PUBLISHER_INDENTATION}.last_valid_index = {glyphs[-1].code},\n'
        output += f'{LFC_PUBLISHER_INDENTATION}.glyph_lut = {options.name}_glyph_lut,\n'
        output += f'{LFC_PUBLISHER_INDENTATION}.glyph_bitmap = {options.name}_glyph_bitmap,\n'
        output += f'{LFC_PUBLISHER_INDENTATION}.glyph_metadata = {options.name}_glyph_metadata,\n'
        output += f'{LFC_PUBLISHER_INDENTATION}.indexing_mode = LUMINA_FONT_INDEXING_MODE_{indexing_mode},\n'
        output += '};'

        return output
