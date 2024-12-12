import os.path
import argparse
import itertools

class LFCOptions:
    def __init__(self) -> None:
        self.bpp = None
        self.name = None
        self.fonts = []

        self.parser = argparse.ArgumentParser()

        self.parser.add_argument(
                '--name',
                type=str,
                required=True,
                help='The name of the generated lumina compatible font')

        self.parser.add_argument(
                '--bpp',
                type=int,
                choices=[1, 2, 4, 8],
                required=True,
                help='Defines how many bits per pixel to use for the generated font')

        self.parser.add_argument(
                '--font',
                type=str,
                required=True,
                action='append',
                nargs=3,
                metavar=('path', 'size', 'character_range'),
                help='The path to the font file to convert, font size (e.g., 12), '
                     'and a list of comma separated character ranges to convert. E.g., '
                     '--font "/path/to/font.ttf" 14 65,66-70')

        self.parser.add_argument(
                '--output',
                type=str,
                required=False,
                help='The path to the generated font file')


    def parse(self) -> None:
        arguments = self.parser.parse_args()

        self.bpp = int(arguments.bpp)
        self.name = arguments.name
        self.output_path = arguments.output

        # Check if the font files exist
        for path, size, character_range in arguments.font:
            if not os.path.isfile(path):
                raise FileNotFoundError('The specified font file does not exist')

            self.fonts.append((path, int(size), self.expand_character_range(character_range), character_range))

        # Group character ranges by font. Used if the same font file is specified multiple times
        # for key, group in itertools.groupby(sorted(arguments.font, key=lambda x: x[0]), lambda x: x[0]):
        #     for _, size, character_range in group:
        #         self.fonts.append((key, int(size), self.expand_character_range(character_range)))


    def parse_int(self, value: str) -> int:
        return int(value, 16 if value.startswith('0x') else 10)


    def expand_character_range(self, characters: str) -> list:
        # Split the comma separated list of character ranges
        tokens = ''.join(characters.split()).split(',')

        character_array = []

        # Parse the single characters or character ranges
        for token in tokens:
            match token.count('-'):
                case 0:
                    character_array.append(self.parse_int(token))
                case 1:
                    start, end = token.split('-')
                    character_array += list(range(self.parse_int(start), self.parse_int(end) + 1))
                case _:
                    raise ValueError(
                            'Invalid character range. '
                            'Use a comma separated list of numbers or ranges of numbers')

        # Remove duplicates and return the list
        return sorted(list(set(character_array)))


    def __str__(self) -> str:
        result = f"Options:\n"
        result += f'  Name: {self.name}\n'
        result += f'  Bits per pixel: {self.bpp}\n'

        for path, size, character_range, _ in self.fonts:
            result += '  Font:\n'
            result += f'    Path: {path}\n'
            result += f'    Size: {size}\n'
            result += f'    Characters: {character_range}\n'

        return result
