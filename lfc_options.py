"""Module for parsing and storing command line arguments"""

import argparse
import os.path
import string

class LFCOptions:
    """Class for parsing and storing command line arguments"""
    def __init__(self):
        self.parse()


    def parse(self):
        """Function that parses the command line arguments"""
        parser = argparse.ArgumentParser('Convert a font file to a Lumina compatible format')

        parser.add_argument(
                '--bpp',
                type=int,
                choices=[1, 2, 4, 8],
                required=True,
                help='Defines how many bits per pixel to use for the generated font')

        parser.add_argument(
                '--name',
                type=str,
                required=True,
                help='The name of the generated lumina compatible font')

        parser.add_argument(
                '--height',
                type=int,
                required=True,
                help='The height of the generated font')

        parser.add_argument(
                '--font',
                type=str,
                required=True,
                help='The path to the font file to convert')

        parser.add_argument(
                '--characters',
                type=str,
                required=True,
                help='A comma separated list of numbers or ranges of characters to convert. '
                     'E.g. 65,66-70,75')

        arguments = parser.parse_args()

        self.bpp = int(arguments.bpp)
        self.name = arguments.name
        self.height = arguments.height

        if not os.path.isfile(arguments.font):
            raise FileNotFoundError('LFC::ERROR: The specified font file does not exist')

        self.font = arguments.font
        self.characters = self.expand_characters(arguments.characters)


    def parse_int(self, value: str):
        """Converts a string into an integer with a base 10 or 16 prefix"""
        return int(value, 16 if value.startswith('0') else 10)

    
    def character_is_valid(self, character: str):
        """Checks if a character is valid"""
        return character.isnumeric() or all(c in string.hexdigits for c in character)


    def expand_characters(self, characters: str):
        """Convert a comma separated list of numbers or ranges of numbers into an integer list"""
        characters = ''.join(characters.split())

        tokens = characters.split(',')

        character_array = []

        for token in tokens:
            match token.count('-'):
                case 0:
                    if not self.character_is_valid(token):
                        raise ValueError(f'LFC::ERROR: Invalid character: {token}. Use a number or a hex value')

                    character_array.append(self.parse_int(token))
                case 1:
                    start, end = token.split('-')

                    if not self.character_is_valid(start):
                        raise ValueError(f'LFC::ERROR: Invalid range start: {start}. Use a number or a hex value')

                    if not self.character_is_valid(end):
                        raise ValueError(f'LFC::ERROR: Invalid range end: {end}. Use a number or a hex value')

                    character_array += list(range(self.parse_int(start), self.parse_int(end) + 1))
                case _:
                    raise ValueError(
                            'LFC::ERROR: Invalid character range. '
                            'Use a comma separated list of numbers or ranges of numbers')

        return character_array


    def __str__(self):
        output = ''

        output += f'name: {self.name}\n'
        output += f'bpp: {self.bpp}\n'
        output += f'height: {self.height}\n'
        output += f'font: {self.font}\n'
        output += f'characters: {', '.join([str(x) for x in self.characters])}\n\n'

        return output
