Python Client Library for HDF5 REST interface
=============================================

The h5pyd package is modeled after `h5py <https://github.com/h5py/h5py>`_ and provides
a largely compatible interface -- most codes developed using h5py should be able to use h5pyd
with minor modifications -- but rather than a wrapper for the HDF5 library, it is a client library
for the `HDF REST interface <https://github.com/HDFGroup/hdf-rest-api>`_.  Being able to access HDF data via
a web API can be useful in a variety of ways: providing remote data access, distributed applications,
utilizing object-based storage (e.g. AWS S3, Azure Blob storage), and many other situations where having to
setup access to HDF5 files on disk would be impractical.

The h5pyd package can be used with the following services:

* `h5serv <https://github.com/HDFGroup/h5serv>`_ (DEPRECATED)
* `hsds <https://github.com/HDFGroup/hsds>`_ - container-based service for Docker and Kubernetes
* `hslambda <https://github.com/HDFGroup/hsds/blob/master/docs/aws_lambda_setup.md>`_ - Serverless implementation using AWS Lambda
* `hsdirect <https:/github.com/HDFGroup/tbd>`_ - direct access to posix or object-storage

Since the server is abstracted behind a http-interface, and service that implements the HDF REST API could be
used as well.

The h5pyd package also includes a set of command line tools (CLI tools) for managing remote data as well.  See: :ref:`apps`


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
    high/folder
    high/group
    high/dataset
    high/attr
    high/dims
    high/table

CLI tools reference
-------------------

.. toctree::
    :maxdepth: 1

    apps/hsinfo
    apps/hsls
    apps/hsload
    apps/hsget
    apps/hstouch
    apps/hsmv
    apps/hscp
    apps/hsdiff
    apps/hsacl


Advanced topics
---------------

.. toctree::
    :maxdepth: 1

    config
    special
    strings
    refs


Meta-info about the h5pyd project
---------------------------------

.. toctree::
    :maxdepth: 1

    whatsnew/index
    contributing
    release_guide
    faq
    h5py_unsupported
    licenses

Don't forget to check these... (development phase only)
-------------------------------------------------------

.. todolist::
