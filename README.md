Converter for BST Hebrew Grabsteine to Unicode
==============================================

This script translates ASCII text written for [BST Hebrew][1] to Unicode.
The bidirectional writing direction is respected,
extensive punctuations are removed,
and the text is normalized (using the [hebrew][2] library).

Installation
------------
In addition to [Python][3], [poetry][4] must be installed.
In the cloned directory, the project can be installed by calling `poetry install`.
This will also install all dependencies.

Usage
-----
To get a help message, run `poetry run start --help`.
To run some (very) basic tests, run `poetry run pytest`.
To translate a Grabsteine-file, run `poetry run start <path/to/file.csv>`.
For each Grabstein, this will translate the hebrew texts
and create an output file in the `output` subdirectory.
The output directory can be changed with the `-o` option.

[1]: https://www.drshirley.org/fonts/BSTHebrew.html
[2]: https://pypi.org/project/hebrew/
[3]: https://www.python.org
[4]: https://python-poetry.org/docs/#installation
