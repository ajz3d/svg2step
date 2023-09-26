# svg2step
This simple program utilizes FreeCAD to batch convert Scalable Vector Graphics (SVG) files to ISO 10303-21 STEP format.

Converted STEP files are saved to the same path as the original SVG files and will overwrite any existing STEP files of the same name.

The program requires existing FreeCAD installation with `freecadcmd` executable in the system `PATH`. 

While `svg2step` was written for GNU/Linux, you can easily modify it to work on any operating system by changing the path stored in `LIST_PATH` variable to point at a temporary directory which you have write permissions to:

``` python
LIST_PATH = Path('/dev/shm/svg2step')
```

## Usage

The program accepts a list of SVG files as arguments:

``` sh
svg2step file1.svg file2.svg ...
```
