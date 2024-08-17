# Lumina Font Converter

A Python script that uses FreeType2 to convert font files into a format compatible with the Lumina library.

The Lumina Font Converter (LFC) allows you to load a font from a file and convert it into C header and source files. These files can then be used with the Lumina library which is designed with embedded systems in mind but is also suitable for larger systems and computers.

## Command Line Options

| Option       | Description |
| ------------ | ----------- |
| `help`       | Show a help message. |
| `bpp`        | Bits per pixel. Defines how many bits are going to be used for rendering each pixel in the glyph. Accepted values: `1`, `2`, `4`, `8` |
| `name`       | The name to be used for the output file names and the definition of the font variable in the C header file. |
| `height`     | The height of the converted font in pixels. This defines the size of the font glyphs. |
| `font`       | The path to the font file. This file will be used to converte the font glyphs. |
| `characters` | The range of characters you wish to include in the font. This can be specified as a continuous range (e.g., `48-57` for digits) or as a comma-separated list. LFC supports both ASCII and Unicode characters, which is particularly useful for converting icons, such as those from Font Awesome. |

## Dependencies

- python 3.x
- [freetype-py](https://github.com/rougier/freetype-py)
  
## Usage Examples

> [!NOTE]
> This section only covers how to use the Lumina Font Converter to convert fonts. For information on how to use the converted fonts in a project with the Lumina library, please refer to the Lumina library documentation.

### ASCII

Let's convert the Montserrat Medium font into C header and source files.

Configuration:
- Bits per pixel: 2
- Font name: montserrat_medium_14
- Font height: 14
- Font file: /path/to/Montserrat-Medium.ttf
- Characters: 32,48-57 - These are the space character (32) and the digits from 0 to 9 (48-57) from the ASCII table.

```bash
python lfc.py --bpp 2 --name montserrat_medium_14 --height 14 --font /path/to/Montserrat-Medium.ttf --characters 32,48-57
```

You should now have two files in the `output` directory: `montserrat_medium_14.h` and `montserrat_medium_14.c`

### Unicode

Let's convert a few icons from the Font Awesome font into C header and source files.

Configuration:
- Bits per pixel: 4
- Font name: font_awesome_solid_18
- Font height: 18
- Font file: /path/to/Font-Awesome-Solid.ttf
- Characters: 0xf00c,0xf04b - These are the check mark (f00c) and play (f04b) icons from Font Awesome Solid.

```bash
python lfc.py --bpp 4 --name font_awesome_solid_18 --height 18 --font /path/to/Font-Awesome-Solid.ttf --characters 0xf00c,0xf04b
```

You should now have two files in the `output` directory: `font_awesome_solid_18.h` and `font_awesome_solid_18.c`

## Contributing

Any contributions to this project are most welcome!

For any suggestions, feature requests, bug reports and questions, feel free to open an issue in this repository's [issue tracker](https://github.com/kostoskistefan/lumina-font-converter/issues).

Pull requests are also encouraged! Do not hesitate to fork this repository, make changes to the code and submit a pull request. Make sure to follow the coding style as much as possible, to make this project as consistent as possible.

## License

This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE) file for details.
