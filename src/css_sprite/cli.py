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
import sys
from functools import partial
from typing import NamedTuple

import jinja2
from PIL import Image
from PIL import ImageColor
from PIL import ImageMode

from . import __version__


class Size(NamedTuple):
    width: int
    height: int


def pack_auto(args):
    images = args.image
    width = max(image.size[0] for image in images)
    height = max(image.size[1] for image in images)
    return pack_fixed(Size(width, height), args)


def pack_fixed(cell_size: Size, args):
    images = args.image
    count = len(images)
    if args.mode:
        mode = args.mode
        if args.verbose:
            print(f'using forced mode {mode!r}')
    else:
        mode = images[0].mode
        if args.verbose:
            print(f'using mode {mode!r} from {images[0]} ({images[0].filename}')
    vertical = args.vertical
    if vertical:
        grid_size = Size(cell_size.width, cell_size.height * count)
    else:
        grid_size = Size(cell_size.width * count, cell_size.height)

    output: Image = Image.new(mode, grid_size, args.background)
    context_images = []
    context = {
        'images': context_images,
        'grid': {
            'vertical': args.vertical,
            'cell': {
                'size': {
                    'width': cell_size.width,
                    'height': cell_size.height,
                },
                'count': count,
            },
            'size': {
                'width': grid_size[0],
                'height': grid_size[1],
            },
        },
        'output': args.output,
    }
    image: Image
    for position, image in enumerate(images):
        x_offset = (cell_size.width - image.size[0]) // 2
        y_offset = (cell_size.height - image.size[1]) // 2
        if vertical:
            x, y = 0, position * cell_size.height
        else:
            x, y = position * cell_size.width, 0
        output.paste(image, (x + x_offset, y + y_offset))
        context_images.append(
            {
                'count': position + 1,
                'filename': image.filename,
                'position': {
                    'x': x,
                    'y': y,
                },
                'offset': {
                    'x': x_offset,
                    'y': y_offset,
                },
                'size': {
                    'x': image.size[0],
                    'y': image.size[1],
                },
            }
        )

    if args.template:
        print(args.template.render(context))

    return output


size_re = re.compile(r'(\d+):(\d+)')


def parse_grid(value):
    if value == 'auto':
        return pack_auto
    elif m := size_re.fullmatch(value):
        return partial(pack_fixed, Size(*map(int, m.groups())))
    else:
        raise argparse.ArgumentTypeError(f'invalid value: {value!r}')


def parse_mode(value):
    try:
        ImageMode.getmode(value)
    except Exception as exc:
        raise argparse.ArgumentTypeError(f'invalid value: {value!r} ({exc!r}, acceptable values: {", ".join(ImageMode._modes.keys())})')
    return value


parser = argparse.ArgumentParser(
    description='Generate a css sprite.',
)
parser.add_argument(
    'image',
    nargs=argparse.ONE_OR_MORE,
    help="Path to image to include in sprite.",
    type=Image.open,
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
    '--mode',
    '-m',
    type=parse_mode,
    help="Force a certain image mode in the output, see: https://pillow.readthedocs.io/en/latest/handbook/concepts.html#modes.",
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
    help="Background color.",
    type=ImageColor.getrgb,
    default=ImageColor.getrgb('#00000000'),
)
template_parser = parser.add_mutually_exclusive_group()
template_parser.add_argument(
    '--template',
    '-t',
    type=jinja2.Template,
    help="Jinja template for CSS output on stdout.",
)
template_parser.add_argument(
    '--template-path',
    '-p',
    type=pathlib.Path,
    help="Jinja template path for CSS output on stdout.",
)
parser.add_argument(
    '--verbose',
    action='store_true',
    help="Make output verbose.",
)
parser.add_argument(
    '--version',
    action='version',
    version=f'%(prog)s {__version__}',
)


def main(args=None):
    args: argparse.Namespace = parser.parse_args(args=args)
    if args.verbose:
        print('parsed arguments:', file=sys.stderr)
        for key, value in args.__dict__.items():
            if isinstance(value, list):
                value = "\n    ".join(map(repr, value))
                print(f'  {key}=[\n    {value}\n  ]', file=sys.stderr)
            else:
                print(f'  {key}={value!r}', file=sys.stderr)
    output = args.grid(args)
    if args.verbose:
        print(f'writing to: {args.output}', file=sys.stderr)
    output.save(str(args.output))
