.. _apps:

hsinfo
======

Usage::

    hsinfo [OPTIONS] [DOMAIN]

Get status information from the server or domain stats if a domain is provided.

Options
--------

-e, --endpoint URL
    HDF REST server endpoint, e.g. http://hsdshdflab.hdfgroup.org
--rescan
    Refresh domain stats (if `DOMAIN` is provided)
-u, --user USERNAME  User name credential
-p, --password PSSWD  Password credential
-b, --bucket BUCKET  Bucket name
-c, --conf CFGFILE   Credential and configuration file
-H, --human-readable  Together with ``-v``, print human readable sizes (e.g. ``123M``)
--logfile LOGFILE   Logfile path
--loglevel LEVEL
    Change log level, one of: ``debug``, ``info``, ``warning``, ``error``.
-h, --help
    Help message

hsload
======

Usage::

    hsload [OPTIONS]  SOURCEFILE  DOMAIN
    hsload [OPTIONS]  SOURCEFILE  FOLDER

Ingest an HDF5 file to a `DOMAIN`, or multiple files to a domain `FOLDER`.

Arguments
----------

`SOURCEFILE`
    HDF5 file to be copied
`DOMAIN`
    HDF Server domain (UNIX or DNS style)
`FOLDER`
    HDF Server folder (UNIX style ending in `/`)

Options
-------

-h, --help  Help message
-v, --verbose   Enable verbose output
-e, --endpoint URL  The HDF Server endpoint, e.g. http://hsdshdflab.hdfgroup.org
-u, --user USERNAME  User name credential
-p, --password PSSWD  Password credential

.. todo:: What are the values of `MODE`?

-a, --append MODE  Flag to append to an existing HDF Server domain
-c, --conf CFGFILE   Credential and configuration file
-z  Compress any non-compressed dataset
--compression ALGO
    Use the given compression algorithm for the ``-z`` option. `ALGO` one of:
    ``blosclz``, ``lz4`` (default), ``lz4hc``, ``snappy``, ``gzip``, ``zstd``.
--cnf-eg  Print the config file and exit.
--logfile LOGFILE   Logfile path
--loglevel LEVEL
    Change log level, one of: ``debug``, ``info``, ``warning``, ``error``.
--bucket BUCKET  Storage bucket
--nodata   Do not upload dataset data
--retries N  Number of server retry attempts
--link
    Link to dataset data (`SOURCEFILE` given as ``<bucket>/<path>``)

    This option enables just the source HDF5 metadata to be ingested while the dataset data
    are left in the original file and fetched as needed.

    When used with files stored in AWS S3, the source file can be specified using the S3
    path: ``s3://<bucket_name>/<s3_path>``. Preferably, the bucket should be in the same
    region as the HSDS service.

    For POSIX or Azure deployments, the source file needs to be copied to a
    regular file system and `hsload` run from a directory that mirrors the
    bucket layout. E.g. if consider a POSIX deployment where the `ROOT_DIR` is
    ``/mnt/data`` and the HSDS default bucket is ``hsdsdata`` (so ingested data
    will be stored in ``/mnt/data/hsdsdata``), the source HDF5 files could be
    stored in ``/mnt/data/hdf5/`` and the file ``myhdf5.h5`` would be imported
    as::

        hsload --link data/hdf5/myhdf5.h5 <folder>

    This option requires HDF5-1.10.6 or later and h5py 2.10 or later.
    The Docker image 'hdfgroup/hdf5lib:1.10.6' includes these versions as well as h5pyd.
    E.g.::

        docker run --rm -v ~/.hscfg:/root/.hscfg  -v ~/data:/data -it hdfgroup/hdf5lib:1.10.6 bash

hsls
====

Usage::

    hsls [OPTIONS] DOMAINS

Example::

    hsls -r -e http://hsdshdflab.hdfgroup.org /shared/tall.h5

Options
-------

-h, --help  Help message
-v, --verbose   Enable verbose output
-H, --human-readable  Together with ``-v``, print human readable sizes (e.g. ``123M``)
-e, --endpoint URL  The HDF Server endpoint, e.g. http://hsdshdflab.hdfgroup.org
-u, --user USERNAME  User name credential
-p, --password PSSWD  Password credential
-c, --conf CFGFILE   Credential and configuration file
--showacls  Print domain ACLs
--showattrs   Print attributes
--pattern  REGEX  List domains that match the given regex
--query QUERY  List domains where the attributes of the root group match the given query string
--logfile LOGFILE   Logfile path
--loglevel LEVEL
    Change log level, one of: ``debug``, ``info``, ``warning``, ``error``.
--bucket BUCKET  Storage bucket
-r, --recursive  Recursively list sub-folders or sub-groups
