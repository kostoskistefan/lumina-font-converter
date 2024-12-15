import os
import itertools
from lfc_glyph import LFCGlyph
from lfc_options import LFCOptions


class LFCPublisher:
    def __init__(self) -> None:
        pass


    def publish(self, glyphs: list[LFCGlyph], descent: int, options: LFCOptions) -> None:
        output = ''

        output += self.publish_header(options)
        output += self.publish_glyph_bitmaps(glyphs)
        output += self.publish_glyph_data(glyphs)
        output += self.publish_character_maps(glyphs)
        output += self.publish_font(glyphs, descent, options)

        with open(f'{options.output_path}/{options.name}.c', 'w') as f:
            f.write(output)


    def publish_header(self, options: LFCOptions) -> str:
        output = '// ---------------------------------------------------------------------------------------------------------------------\n'

        output += f'// Name: {options.name}\n'
        output += f'// Bits per pixel: {options.bpp}\n'
        output += '// Fonts:\n'

        for path, size, _, character_range in options.fonts:
            output += f'//     Font: {os.path.basename(path)}\n'
            output += f'//     Size: {size}\n'
            output += f'//     Characters: {character_range}\n'

            if path != options.fonts[-1][0]:
                output += '\n'

        output += '// ---------------------------------------------------------------------------------------------------------------------\n\n'

        output += '#include "lumina_font.h"\n\n'

        return output


    def publish_glyph_bitmaps(self, glyphs: list[LFCGlyph]) -> str:
        output = 'static const uint8_t glyph_bitmap[] = {\n'

        for i in range(len(glyphs)):
            output += glyphs[i].publish_bitmap()

            if i < len(glyphs) - 1:
                output += '\n\n'

        output += '\n};\n\n'

        return output


    def publish_glyph_data(self, glyphs: list[LFCGlyph]) -> str:
        output = 'static const lumina_font_glyph_data_t glyph_data[] = {\n'

        output += '    { .bitmap_index = 0, .width = 0, .height = 0, .advance = 0, .y_bearing = 0 }, // Reserved by Lumina\n'

        for i in range(len(glyphs)):
            output += glyphs[i].publish_metadata()

            if i < len(glyphs) - 1:
                output += '\n'

        output += '\n};\n\n'

        return output


    def publish_character_maps(self, glyphs: list[LFCGlyph]) -> str:
        output = ''

        character_groups = self.split_non_consecutive_characters(glyphs)

        ascii_character_groups = []
        unicode_character_group = []

        for group in character_groups:
            if all(glyph.codepoint < 128 for glyph in group):
                ascii_character_groups.append(group)

            else:
                unicode_character_group.extend(group)

        unicode_character_group = sorted(unicode_character_group, key=lambda x: x.codepoint)

        if unicode_character_group != []:
            output += 'static const lumina_utf8_unicode_codepoint_t unicode_codepoints[] = {\n    '

            for i in range(len(unicode_character_group)):
                output += f'0x{unicode_character_group[i].codepoint:04x}, '
                if (i + 1) % 10 == 0 and i < len(unicode_character_group) - 1:
                    output += '\n    '

            output += '\n};\n\n'


        glyph_bitmap_start_index = 1

        output += 'static const lumina_font_character_map_t character_maps[] = {\n'

        for character_group in ascii_character_groups:
            group_length = len(character_group)

            output += '    {\n'
            output += f'        .range_start = {character_group[0].codepoint},\n'
            output += f'        .range_length = {character_group[-1].codepoint - character_group[0].codepoint + 1},\n'
            output += f'        .glyph_bitmap_start_index = {glyph_bitmap_start_index},\n'
            output += f'        .unicode_codepoints = NULL,\n'
            output += f'        .unicode_codepoints_count = 0,\n'
            output += f'        .type = LUMINA_FONT_CHARACTER_MAP_TYPE_SEQUENTIAL,\n'
            output += '    },\n'

            glyph_bitmap_start_index += group_length

        if unicode_character_group != []:
            output += '    {\n'
            output += f'        .range_start = {unicode_character_group[0].codepoint},\n'
            output += f'        .range_length = {unicode_character_group[-1].codepoint - character_group[0].codepoint + 1},\n'
            output += f'        .glyph_bitmap_start_index = {glyph_bitmap_start_index},\n'
            output += f'        .unicode_codepoints = unicode_codepoints,\n'
            output += f'        .unicode_codepoints_count = {len(unicode_character_group)},\n'
            output += f'        .type = LUMINA_FONT_CHARACTER_MAP_TYPE_SPARSE,\n'
            output += '    },\n'

        output += '};\n\n'

        return output


    def publish_font(self, glyphs: list[LFCGlyph], descent: int, options: LFCOptions) -> str:
        character_maps_count = len(self.split_non_consecutive_characters(glyphs))

        output = f'const lumina_font_t {options.name} = {{\n'
        output += f'    .height = {max(glyphs, key=lambda x: x.height).height},\n'
        output += f'    .descent = {descent},\n'
        output += f'    .bits_per_pixel = {options.bpp},\n'
        output += f'    .bitmap = glyph_bitmap,\n'
        output += f'    .glyph_data = glyph_data,\n'
        output += f'    .character_maps = character_maps,\n'
        output += f'    .character_maps_count = {character_maps_count},\n'
        output += '};\n'

        return output


    def split_non_consecutive_characters(self, glyphs: list[LFCGlyph]) -> list[list[LFCGlyph]]:
        out = []

        for _, g in itertools.groupby(enumerate(glyphs), lambda x: x[0] - x[1].codepoint):
            out.append([v for _, v in g])

        return out
