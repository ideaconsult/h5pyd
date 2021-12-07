HDF5 RESTful API for Python
===========================

The h5pyd package is a Pythonic interface to the HDF5 RESTful application
programming interface (API).

`HDF5 <https://www.hdfgroup.org/solutions/hdf5/>`_ lets you store huge amounts
of numerical data, and easily manipulate that data from NumPy. For example, you
can slice into multi-terabyte datasets, as if they were real NumPy arrays.
Thousands of datasets can be stored in a single file object, categorized and
tagged however you want.


Where to start
--------------

* :ref:`Quick-start guide <quick>`
* :ref:`Installation <install>`


Other resources
---------------

* `GitHub project <https://github.com/HDFGroup/h5pyd>`_
* `Ask questions on the HDF Group Forum at <https://forum.hdfgroup.org/c/hsds>`_
* `Python and HDF5 O'Reilly book <https://shop.oreilly.com/product/0636920030249.do>`_


Introductory info
-----------------

.. toctree::
    :maxdepth: 1

    quick
    build


High-level API reference
------------------------

.. toctree::
    :maxdepth: 1

    high/file
    high/group
    high/dataset
    high/attr
    high/dims
    high/lowlevel


Advanced topics
---------------

.. toctree::
    :maxdepth: 1

    config
    special
    strings
    refs
    mpi
    swmr
    vds


Meta-info about the h5py project
--------------------------------

.. toctree::
    :maxdepth: 1

    whatsnew/index
    contributing
    release_guide
    faq
    licenses
