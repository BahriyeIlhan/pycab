# pycab (CArbon Benchmarking)

A python tool for calculating the embodied carbon of [IFC files](https://technical.buildingsmart.org/standards/ifc/).

## Installation

Prerequisites:
* python3 (tested `v3.9`)
* [ifcopenshell](https://github.com/IfcOpenShell/IfcOpenShell) (built with python bindings)
* [markdown](https://python-markdown.github.io/)
* [matplotlib](https://matplotlib.org/)
* [numpy](https://numpy.org/)
* [seaborn](https://seaborn.pydata.org/)
* [pandas](https://pandas.pydata.org/)
* [tabulate](https://pypi.org/project/tabulate/)

pycab is a simple script, no installation is necessary.

## Usage

Example:
```shell
python3 pycab.py --ifcfile examples/EC_Project_SR.ifc
```

Output:
```shell
Processing Project...
Processing Walls...
Processing Slabs/Roofs...
Processing Doors...
Processing Windows/Skylights...
Processing Stairs...
Processing Replacements...
WARNING: did not find material Internal Door Composite in database
WARNING: did not find material Window Composite in database
WARNING: did not find material External Door Composite in database
WARNING: did not find material Stair Composite in database
```

The report is written to the `reports` directory.
