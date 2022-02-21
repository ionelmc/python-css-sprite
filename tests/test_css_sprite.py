from pathlib import Path

import pytest

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
    ],
)
def test_run(output_file: Path, args, expected_output_file):
    main(['tests/red.png', 'tests/big-red.png', 'tests/green.png', 'tests/big-green.png', 'tests/blue.png', '-o', str(output_file), *args])
    with open(expected_output_file, 'rb') as expected:
        assert output_file.read_bytes() == expected.read()
