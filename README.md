# liboqs-bench: a small Python benchmark utility for the liboqs-python library

## About

Small Python utility benchmarking PQC KEM algorithms and schemes from the `liboqs-python` library by Open Quantum Safe. The program measures each algorithm step separately for as many schemes as required by running the step a specified number of iterations for five trials in total. It then chooses the fastest trial and calculates the average.

This is a hobby project and not meant for production environments.

## Prerequisites

`liboqs-bench` requires `liboqs` and `liboqs-python` from Open Quantum Safe to be installed. Go to their [Github](https://github.com/open-quantum-safe/liboqs-python) for instructions.

## Installation (optional)

Execute

`pip install path/to/liboqs_bench-0.1.0-py3-none-any.whl`

Afterwards `liboqs_bench` can be [run from command line](#run-package-from-command-line) or [imported as package](#import-as-package) from anywhere in the environment.

Alternatively, you can include `liboqs_bench/src` into the `PYTHONPATH` variable:

`export PYTHONPATH = $PYTHONPATH:/path/to/liboqs-bench/src`

Or execute the following commands in the directory containing the `liboqs_bench` package (not the `liboqs-bench` project directory).

## Usage

You can run `liboqs_bench` either as script from the command line or import it as package.

### Run package from command line

`liboqs_bench [-h] [-i int] [-l] [-d] [-v] [algorithm] [scheme ...]`

or

`python3 -m liboqs_bench [-h] [-i int] [-l] [-d] [-v] [algorithm] [scheme ...]`

positional arguments:
  algorithm             the desired algorithm step or "complete": \['KeyGeneration', 'Encapsulation', 'Decapsulation', 'complete']
  scheme                at least one KEM scheme or "all" - for full list use -l option

options:
  -h, --help            show this help message and exit
  -i int, --iterations int
                        set the number of iterations of each benchmark trial (default=1000)
  -l, --list-schemes    print the full list of supported KEM schemes
  -d, --debug           set log level to DEBUG and enable oqs warnings and logs (STUB FUNCTIONALITY)
  -v, --version         show program's version number and exit

### Import into Python programs or interpreter

```
>>> from liboqs_bench import liboqs_bench
>>> liboqs_bench({'help'|'schemes'|algorithm} [,scheme1[,scheme2[,scheme3,...]]] [,iterations=int])
```

First argument is the algorithm step: "KeyGeneration", "Encapsulation", "Decapsulation", or "complete".

After the first argument, as many scheme names as desired can be provided as positional arguments or
the argument "all" in order to compare all schemes with each other.

Finally, the user can provide an integer as keyword argument "iterations" to specify the number of 
iterations each benchmark round should use. The default number is 1000.

For help, the user can pass as the first argument "help", which prints out this docstring, or "schemes", 
which returns a list of supported KEM schemes.

# Development

Development files are under `liboqs-bench/dev` including `requiremments.txt` and Jupyter Notebooks. `liboqs` and `liboqs-python` need to be installed manually.

# Acknowledgements

Credits to [Open Quantum Safe](https://github.com/open-quantum-safe) for their amazing work in the field of post-quantum cryptography.

# License

GPL-3.0-or-later (GNU General Public License v3.0 or later). See LICENSE.txt for specifics.
