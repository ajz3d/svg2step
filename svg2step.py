#!/usr/bin/python3
"""Converts SVG files to STEP files using FreeCAD.

This module allows to convert 2D scalable vector graphics files
to ISO 10303-21 STEP files using freecadcmd.

The program outputs STEP files in the same path as input SVG files,
overwriting any existing STEP file of the same name.

Typical usage:

    ``svg2step.py svg_file1 svg_file2 svg_file3``

"""
import argparse
import subprocess
import sys
from pathlib import Path
try:
    import FreeCAD
    import FreeCAD.Draft
    import Import
    import importSVG
except ModuleNotFoundError:
    FREECAD = False
else:
    FREECAD = True


LIST_PATH = Path('/dev/shm/svg2step')


def batch():
    """Collects input file paths and sends them for conversion."""
    if not LIST_PATH.parent.exists():
        print(f'Path not found: {LIST_PATH.parent}')
        sys.exit(1)
    parser = argparse.ArgumentParser(
        prog='svg2step batch list provider',
        description='Converts SVG files to STEP using FreeCAD.',
    )
    parser.add_argument(
        'input_files', nargs='*',
        type=Path,
    )
    # Display full help when no arguments are provided.
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    source_paths = args.input_files
    for path in source_paths:
        step_path = Path(path.parent, Path(f'{path.stem}.stp'))
        # Paths of input SVG files as well as output STEP paths need
        # to be stored in a file to be accessible by the script instance
        # executed from freecadcmd.
        with open(LIST_PATH, 'w', encoding='utf-8') as file:
            file.write(f'{str(path)}\n')
            file.write(f'{str(step_path)}\n')
        subprocess.run(
            f'freecadcmd {__file__}',
            check=True,
            shell=True,
            text=True,
            universal_newlines=True
        )
    LIST_PATH.unlink(missing_ok=True)


def convert():
    """Performs conversion operation within FreeCAD."""
    with open(LIST_PATH, 'r', encoding='utf-8') as file:
        svg = Path(file.readline().rstrip())
        step = Path(file.readline().rstrip())
    importSVG.open(svg)
    objects = FreeCAD.activeDocument().Objects
    Import.export(objects, str(step))


if FREECAD:
    convert()
else:
    batch()
