"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mcss_sprite` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``css_sprite.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``css_sprite.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse
import pathlib
import re
from dataclasses import dataclass

import jinja2
from PIL import Image
from PIL import ImageColor


def pack_auto(args):
    images = args.image
    width = max(image.size[0] for image in images)
    height = max(image.size[1] for image in images)
    return pack_to_size(width, height)(args)


@dataclass
class pack_to_size:
    width: int
    height: int

    def __call__(self, args):
        images = args.image
        count = len(images)
        mode = images[0].mode
        vertical = args.vertical
        if vertical:
            size = self.width, self.height * count
        else:
            size = self.width * count, self.height

        output = Image.new(mode, size, args.background)
        context_images = []
        context = {
            'images': context_images,
            'width': self.width,
            'height': self.height,
            'output': {
                'path': args.output,
                'count': count,
            },
        }
        image: Image
        for position, image in enumerate(images):
            x_offset = (self.width - image.size[0]) // 2
            y_offset = (self.height - image.size[1]) // 2
            if vertical:
                x, y = 0, position * self.height
            else:
                x, y = position * self.width, 0
            output.paste(image, (x + x_offset, y + y_offset))
            context_images.append(
                {
                    'count': position + 1,
                    'x': x,
                    'y': y,
                    'filename': image.filename,
                    'x_offset': x_offset,
                    'y_offset': y_offset,
                }
            )

        if args.template:
            print(args.template.render(context))

        return output


def parse_image(value):
    return Image.open(value)


size_re = re.compile(r'(\d+):(\d+)')


def parse_grid(value):
    if value == 'auto':
        return pack_auto
    elif m := size_re.fullmatch(value):
        return pack_to_size(*map(int, m.groups()))
    else:
        raise argparse.ArgumentTypeError(f'invalid value: {value!r}')


parser = argparse.ArgumentParser(
    description='Generate a css sprite.',
)
parser.add_argument(
    'image',
    nargs=argparse.ONE_OR_MORE,
    help="Path to image to include in sprite.",
    type=parse_image,
)
parser.add_argument(
    '--grid',
    '-g',
    help="Grid cell size to use. One of: auto, X:Y.",
    type=parse_grid,
    default=pack_auto,
)
parser.add_argument(
    '--output',
    '-o',
    help="Output file.",
    type=pathlib.Path,
    required=True,
)
parser.add_argument(
    '--vertical',
    '-v',
    help="Stack the images vertically (they are stacked horizontally by default).",
    action='store_true',
)
parser.add_argument(
    '--background',
    '-b',
    help="Background.",
    type=ImageColor.getrgb,
    default=ImageColor.getrgb('#ffffffff'),
)
parser.add_argument(
    '--template',
    '-t',
    type=jinja2.Template,
    help="Jinja template for CSS output on stdout.",
)


def main(args=None):
    args = parser.parse_args(args=args)
    output = args.grid(args)
    output.save(str(args.output))
