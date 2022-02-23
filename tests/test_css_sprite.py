from pathlib import Path

import pytest
from PIL import Image

from css_sprite.cli import Size
from css_sprite.cli import main


@pytest.fixture
def output_file(tmp_path_factory):
    return tmp_path_factory.mktemp("data") / "output.png"


@pytest.mark.parametrize(
    'args,expected_output_file',
    [
        ((), 'tests/output.png'),
        (('-g', '5:5'), 'tests/output-5x5.png'),
        (('-g', '50:50'), 'tests/output-50x50.png'),
        (('-g', '50:50', '-m', 'RGBA'), 'tests/output-50x50.png'),
    ],
)
def test_run(output_file: Path, args, expected_output_file):
    main(['tests/red.png', 'tests/big-red.png', 'tests/green.png', 'tests/big-green.png', 'tests/blue.png', '-o', str(output_file), *args])
    with open(expected_output_file, 'rb') as expected:
        assert output_file.read_bytes() == expected.read()


def test_size_interface():
    assert tuple(Size(1, 2)) == (1, 2)
    assert Image.new("RGBA", Size(1, 2)).size == (1, 2)
