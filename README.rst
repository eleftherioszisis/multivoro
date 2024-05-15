.. image:: https://github.com/eleftherioszisis/multivoro/blob/main/logo.png

Parallel cell-based 3D voronoi tessellations
--------------------------------------------

multivoro is a python library that allows building 3D Voronoi/Laguerre tessellations with `voro++ <voro_site_>`_ exposed in python via the nanobind_ library.
It leverages the latest `multi-threaded extension of Voro++ <voro_mthread_>`_ to allow computing the voronoi cells in parallel.

Codebases
---------
* `Voro++ <voro_repo_>`_
* nanobind_

Installation
------------

Wheels
~~~~~~
There are available pre-compiled wheels to pip install for Linux and macOS.
However, note that these wheels are compiled without multithreading support.

To install them in your system:

.. code-block:: bash

  pip install multivoro

Source
~~~~~~
To build multivoro from source in Ubuntu:

Setup a python virtual environment:

.. code-block:: bash

   # python versions to choose from: [python3.8-python3.12]
   sudo apt install python3.10-dev python3.10-venv
   python3.10 -mvenv venv
   source ./venv/bin/activate

Install openmp runtime and compile the wheel:

.. code-block:: bash

   sudo apt install libomp-dev
   git clone --recurse-submodules https://github.com/eleftherioszisis/multivoro.git
   cd multivoro
   USE_OpenMP=ON pip install .

USE_OpenMP environment variable is used as an option in multivoro cmake. By default it is set to 'OFF'.

Usage
-----

.. code-block:: python

   from multivoro import compute_voronoi

   cells = compute_voronoi(
       points=[[-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
       radii=[1.0, 1.0],
       limits=[[-2.0, -1.0, -1.0], [2.0, 1.0, 1.0]],
       n_threads=6,
   )

   for cell in cells:
       print(cell.get_vertices())
       print(cell.get_neighbors())
       print(cell.get_face_vertices())

Voro++ Copyright And Acknowledgments
------------------------------------

Copyright Notice
~~~~~~~~~~~~~~~~

Voro++ Copyright (c) 2008, The Regents of the University of California, through
Lawrence Berkeley National Laboratory (subject to receipt of any required
approvals from the U.S. Dept. of Energy). All rights reserved.

If you have questions about your rights to use or distribute this software,
please contact Berkeley Lab's Technology Transfer Department at TTD@lbl.gov.

NOTICE. This software was developed under partial funding from the U.S.
Department of Energy. As such, the U.S. Government has been granted for itself
and others acting on its behalf a paid-up, nonexclusive, irrevocable, worldwide
license in the Software to reproduce, prepare derivative works, and perform
publicly and display publicly. Beginning five (5) years after the date
permission to assert copyright is obtained from the U.S. Department of Energy,
and subject to any subsequent five (5) year renewals, the U.S. Government is
granted for itself and others acting on its behalf a paid-up, nonexclusive,
irrevocable, worldwide license in the Software to reproduce, prepare derivative
works, distribute copies to the public, perform publicly and display publicly,
and to permit others to do so.


Acknowledgments
~~~~~~~~~~~~~~~
This work (voro++) was supported by the Director, Office of Science, Computational and
Technology Research, U.S. Department of Energy under Contract No.
DE-AC02-05CH11231.


.. _voro_repo: https://github.com/chr1shr/voro
.. _voro_site: http://math.lbl.gov/voro++/
.. _voro_mthread: https://doi.org/10.1016/j.cpc.2023.108832
.. _nanobind: https://github.com/wjakob/nanobind
