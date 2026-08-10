# liboqs-bench: a small Python benchmark utility for the liboqs-python library

## About

Small Python utility benchmarking PQC KEM algorithms and schemes from the [liboqs-python library by Open Quantum Safe](https://github.com/open-quantum-safe/liboqs-python). The program measures each algorithm step separately for as many schemes as required by running the step a specified number of iterations for five trials in total. It then chooses the fastest trial and calculates the average.

This is a hobby project and not meant for production environments.

## Prerequisites

`liboqs-bench` requires `liboqs` and `liboqs-python` from Open Quantum Safe to be installed. Go to their [Github](https://github.com/open-quantum-safe/liboqs-python) for instructions.

## Installation (optional)

Execute

`pip install path/to/liboqs_bench-0.2.0-py3-none-any.whl`

Afterwards `liboqs_bench` and `liboqs_bench_client` can be [run from command line](#run-package-from-command-line) or [imported as package](#import-as-package) from anywhere in the environment.

Alternatively, you can include `liboqs_bench/src` into the `PYTHONPATH` variable:

`export PYTHONPATH = $PYTHONPATH:/path/to/liboqs-bench/src`

Or execute the following commands in the `src` directory (only for running as Python module or import, not as command line prompt.)

## Usage of main utility

You can run `liboqs_bench` and `liboqs_bench_client` either from the command line or import it into a Python environment.

### Run from command line

`liboqs_bench [-h] [-d] [-H HOST] [-i] [-I int] [-l] [-P PORT] [-s] [-v] [algorithm] [schemes ...]`

or as Python module

`python3 -m liboqs_bench [-h] [-d] [-H HOST] [-i] [-I int] [-l] [-P PORT] [-s] [-v] [algorithm] [schemes ...]`

positional arguments:
  algorithm             the desired algorithm step or "complete": \['KeyGeneration', 'Encapsulation', 'Decapsulation', 'complete']
  scheme                at least one KEM scheme or "all" - for full list use -l option

options:
  -h, --help            show this help message and exit
  -d, --debug           set log level to DEBUG and enable oqs warnings and logs (STUB FUNCTIONALITY)
  -H HOST, --host HOST  IP address of host server interface (127.0.0.1 by default)
  -i, --info            set log level to INFO and enable oqs warnings and logs (STUB FUNCTIONALITY)
  -I int, --iterations int
                        set the number of iterations of each benchmark trial (default=1000)
  -l, --list-schemes    print the full list of supported KEM schemes and exit
  -P PORT, --port PORT  registered port (1024-49151) on which to expose service (default=31021)
  -s, --server          expose liboqs_bench as network service
  -v, --version         show program's version number and exit
  
### Run in Python environment

```
>>> from liboqs_bench import liboqs_bench
>>> liboqs_bench({'help'|'schemes'|'server'|algorithm} [,host,port] [,scheme1[,scheme2[,scheme3,...]]] [,iterations=int])
```

First argument is the algorithm step: "KeyGeneration", "Encapsulation", "Decapsulation", or "complete".

After the first argument, as many scheme names as desired can be provided as positional arguments or the argument "all" in order to compare all schemes with each other.

Finally, the user can provide an integer as keyword argument "iterations" to specify the number of iterations each benchmark round should use. The default number is 1000.

For help, the user can pass as the first argument "help", or "schemes",  which returns a list of supported KEM schemes.

### Start a server

Start a server with one of these options:

`liboqs_bench -s -H HOST -P PORT`, or

`python3 -m liboqs_bench -s -H HOST -P PORT`, or

`liboqs_bench('server', 'HOST', PORT)` (in a Python environment).

## Usage of client function

### Run from command line

`liboqs_bench_client [-h] [-d] [-H HOST] [-i] [-I int] [-l] [-P PORT] [-v] [algorithm] [schemes ...]`

positional arguments:
  algorithm             the desired algorithm step or "complete": ['KeyGeneration', 'Encapsulation', 'Decapsulation', 'complete']
  schemes               at least one KEM scheme or "all" - for full list use -l option

options:
  -h, --help            show this help message and exit
  -d, --debug           set log level to DEBUG
  -H HOST, --host HOST  IP address of host server interface (127.0.0.1 by default)
  -i, --info            set log level to INFO
  -I int, --iterations int
                        set the number of iterations of each benchmark trial (default=1000)
  -l, --list-schemes    print the full list of supported KEM schemes and exit
  -P PORT, --port PORT  registered port (1024-49151) on which to expose service (default=31021)
  -v, --version         show program's version number and exit

### Run in Python environment

```
>>> from liboqs_bench_client import liboqs_bench_client
>>> liboqs_bench_client({'help'|host} [,port] [,alg] [,scheme1[,scheme2[,scheme3,...]]] [,iterations=int])

```

First two arguments are host and port address of the server.

Then comes the algorithm step: "KeyGeneration", "Encapsulation", "Decapsulation", or "complete".

Afterwards as many scheme names as desired can be provided as positional arguments or the argument "all" in order to compare all schemes with each other.

Finally, the user can provide an integer as keyword argument "iterations" to specify the number of iterations each benchmark round should use. The default number is 1000.

For help, the user can pass as the first argument "help".

# Development

Development files are under `liboqs-bench/dev` including `requiremments.txt` and Jupyter Notebooks. `liboqs` and `liboqs-python` need to be installed manually (see [Prerequisites](#prerequisites)).

# Acknowledgements

Credits to [Open Quantum Safe](https://github.com/open-quantum-safe) for their amazing work in the field of post-quantum cryptography.

# License

GPL-3.0-or-later (GNU General Public License v3.0 or later). See LICENSE.txt for specifics.
