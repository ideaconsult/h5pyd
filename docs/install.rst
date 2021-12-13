.. _install:

Installation
============

h5pyd is a pure Python package without dependency on the HDF5 library.
Installing it is as easy as::

    $ pip install h5pyd

If installing inside a virtual environment make sure to use its own `pip`.


.. _source_install:

Source Installation
-------------------

There are two options to install h5pyd from source:

* Download a ZIP archive from https://github.com/HDFGroup/h5pyd

  1. Unzip the archive.
  2. Change to the top folder created after unzipping.
  3. Run::

      $ pip install .

* Install directly from https://github.com/HDFGroup/h5pyd::

    $ pip install git+https://github.com/HDFGroup/h5pyd.git

  (`git` command-line tool is required.)


.. _dev_install:

Development Installation
........................

Assuming the `git` command-line tool is available, run:

.. code-block:: shell

    $ git clone https://github.com/HDFGroup/h5pyd.git
    $ cd h5pyd
    $ pip install -e .

Verify the installation by executing the test suite::

    $ python testall.py

.. tip::
    Sometimes it may be necessary to discard everything but the code committed
    to git. In the top folder of the h5pyd repo, run::

    $ git clean -xfd
