import argparse
import os.path

class LFCOptions:
    def __init__(self):
        self.parse()


    def parse(self):
        parser = argparse.ArgumentParser(description='Convert a TTF font file to C code used by the Lumina library')
        parser.add_argument('--bpp', type=int, choices=[1, 2, 4, 8], required=True, help='Defines how many bits per pixel to use for the generated font')
        parser.add_argument('--name', type=str, required=True, help='The name of the generated lumina compatible font')
        parser.add_argument('--height', type=int, required=True, help='The height of the generated font')
        parser.add_argument('--font', type=str, required=True, nargs=2, metavar=('font_file', 'characters'), help='The path to the font file to convert and a list of comma separated list of numbers or ranges of characters to convert. E.g. 65,66-70,75')

        arguments = parser.parse_args()

        self.bpp = int(arguments.bpp)
        self.name = arguments.name
        self.height = arguments.height

        if not os.path.isfile(arguments.font[0]):
            raise Exception('The specified font file does not exist')

        self.font = arguments.font[0]
        self.characters = self.expand_characters(arguments.font[1])


    def parse_int(self, value: str):
        return int(value, 16 if value.startswith('0') else 10)


    def expand_characters(self, characters: str):
        characters = ''.join(characters.split())

        tokens = characters.split(',')

        character_array = []

        for token in tokens:
            match token.count('-'):
                case 0:
                    character_array.append(self.parse_int(token))
                case 1:
                    start, end = token.split('-')
                    character_array += list(range(self.parse_int(start), self.parse_int(end) + 1))
                case _:
                    raise Exception('Invalid character range. Use a comma separated list of numbers or ranges of numbers')

        return character_array


    def __str__(self):
        output = ''

        output += 'name: {}\n'.format(self.name)
        output += 'bpp: {}\n'.format(self.bpp)
        output += 'height: {}\n'.format(self.height)
        output += 'Fonts: \n'

        for font in self.fonts:
            output += '\tfont: {}\n'.format(font['font'])
            output += '\tcharacters: {}\n\n'.format(', '.join([str(x) for x in font['characters']]))

        return output

