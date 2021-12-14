=============================================
Python Client Library for HDF5 REST Interface
=============================================

The h5pyd package is a client library for the `HDF REST interface
<https://github.com/HDFGroup/hdf-rest-api>`_. It represents an alternative to
the HDF5 library when paired with the following services:

* `hsds <https://github.com/HDFGroup/hsds>`_ - container-based service for Docker and Kubernetes
* `hslambda <https://github.com/HDFGroup/hsds/blob/master/docs/aws_lambda_setup.md>`_ - Serverless implementation using AWS Lambda
* `hsdirect <https:/github.com/HDFGroup/tbd>`_ - direct access to POSIX file systems or object storage
* `h5serv <https://github.com/HDFGroup/h5serv>`_ **(DEPRECATED)**

However, any web service that implements the HDF REST API could be used as well.

Being able to access HDF data via a web API can be useful in a variety of ways:
providing remote data access, distributed applications, utilizing object-based
storage (e.g. AWS S3, Azure Blob storage), and many other situations where
providing file system access to HDF5 data would be impractical.

The h5pyd package also includes a set of command line tools (CLI tools) for
managing remote data. See :ref:`cli_docs`.

h5pyd package is modeled after `h5py <https://docs.h5py.org>`_.  Software
developed using h5py should be able to use h5pyd with no or only minor
modifications. h5pyd developers express their gratitude to the h5py project for
developing so functional API and great documentation which served as the
template for this one.

.. caution::
    This documentation is work in progress and mistakes or incosistencies are
    possible. Please report them at https://github.com/HDFGroup/h5pyd. Pull
    requests are even better!


Where to Start
--------------

.. toctree::
    :maxdepth: 1

    install
    quick


Other Resources
---------------

* `h5pyd GitHub project <https://github.com/HDFGroup/h5pyd>`_
* `Ask questions on the HDF Group Forum <https://forum.hdfgroup.org/c/hsds>`_
* Andrew Collette's `Python and HDF5 O'Reilly book <https://shop.oreilly.com/product/0636920030249.do>`_


API Documentation
-----------------

.. toctree::
    :maxdepth: 1

    high/file
    high/group
    high/dataset
    high/attr
    high/dims
    high/folder
    high/table

.. _cli_docs:

CLI Tools Documentation
-----------------------

.. toctree::
    :maxdepth: 1

    apps


Advanced Topics
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
    faq
    h5py_unsupported
    licenses


Don't forget to check these... (development phase only)
-------------------------------------------------------

.. todolist::
