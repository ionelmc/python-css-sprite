========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions| |requires|
        | |coveralls| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-css-sprite/badge/?style=flat
    :target: https://python-css-sprite.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/ionelmc/python-css-sprite/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/ionelmc/python-css-sprite/actions

.. |requires| image:: https://requires.io/github/ionelmc/python-css-sprite/requirements.svg?branch=main
    :alt: Requirements Status
    :target: https://requires.io/github/ionelmc/python-css-sprite/requirements/?branch=main

.. |coveralls| image:: https://coveralls.io/repos/ionelmc/python-css-sprite/badge.svg?branch=main&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/ionelmc/python-css-sprite

.. |codecov| image:: https://codecov.io/gh/ionelmc/python-css-sprite/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://codecov.io/github/ionelmc/python-css-sprite

.. |version| image:: https://img.shields.io/pypi/v/css-sprite.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/css-sprite

.. |wheel| image:: https://img.shields.io/pypi/wheel/css-sprite.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/css-sprite

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/css-sprite.svg
    :alt: Supported versions
    :target: https://pypi.org/project/css-sprite

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/css-sprite.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/css-sprite

.. |commits-since| image:: https://img.shields.io/github/commits-since/ionelmc/python-css-sprite/v0.1.1.svg
    :alt: Commits since latest release
    :target: https://github.com/ionelmc/python-css-sprite/compare/v0.1.1...main

.. end-badges

A simple css sprite generator.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install css-sprite

You can also install the in-development version with::

    pip install https://github.com/ionelmc/python-css-sprite/archive/main.zip

Usage
=====

To generate a css sprite from images::

    css-sprite [-h] [--grid GRID] --output OUTPUT
        [--mode MODE] [--vertical] [--background BACKGROUND]
        [--template TEMPLATE | --template-path TEMPLATE_PATH]
        [--verbose] [--version] image [image ...]

Output is mainly a new image but you can also generate the accompanying css.

Positional arguments:
  image                 Path to image to include in sprite.

Options:
  -h, --help            show this help message and exit
  --grid GRID, -g GRID  Grid cell size to use. One of: auto, X:Y.
  --output OUTPUT, -o OUTPUT
                        Output file.
  --mode MODE, -m MODE  Force a certain image mode in the output, see: https://pillow.readthedocs.io/en/latest/handbook/concepts.html#modes.
  --vertical, -v        Stack the images vertically (they are stacked horizontally by default).
  --background BACKGROUND, -b BACKGROUND
                        Background color.
  --template TEMPLATE, -t TEMPLATE
                        Jinja template for CSS output on stdout.
  --template-path TEMPLATE_PATH, -p TEMPLATE_PATH
                        Jinja template path for CSS output on stdout.
  --verbose             Make output verbose.
  --version             show program's version number and exit


Documentation
=============


https://python-css-sprite.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
