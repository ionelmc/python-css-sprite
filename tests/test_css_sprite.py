from pathlib import Path

import pytest
from PIL import Image

from css_sprite.cli import Size
from css_sprite.cli import main

test_dir = Path(__file__).parent


@pytest.mark.parametrize(
    'args,output_file',
    [
        ((), 'output.png'),
        (('-g', '5:5'), 'output-5x5.png'),
        (('-g', '50:50'), 'output-50x50.png'),
        (('-g', '50:50', '-m', 'RGBA'), 'output-50x50.png'),
    ],
)
def test_run(tmp_path, args, output_file, image_diff):
    output_file = str(tmp_path / output_file)
    main(['tests/red.png', 'tests/big-red.png', 'tests/green.png', 'tests/big-green.png', 'tests/blue.png', '-o', output_file, *args])
    image_diff(output_file, str(test_dir.joinpath(output_file)))


def test_size_interface():
    assert tuple(Size(1, 2)) == (1, 2)
    assert Image.new("RGBA", Size(1, 2)).size == (1, 2)
