.. _cli:

CLI Tools
^^^^^^^^^

.. contents::
    :local:
    :depth: 1
    :this-will-duplicate-information-and-it-is-stilluseful-here:

hsinfo
======

Usage::

    hsinfo [ OPTIONS ] [DOMAIN]

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

    hsload [ OPTIONS ]  SOURCEFILE  DOMAIN
    hsload [ OPTIONS ]  SOURCEFILE  FOLDER

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

    hsls [ OPTIONS ] DOMAINS

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


hstouch
=======

Usage::

    hstouch [ OPTIONS ] DOMAINS

Example::

    hstouch -e  http://hsdshdflab.hdfgroup.org  /home/myfolder/emptydomain.h5

Options
-------

-h, --help  Help message
-v, --verbose   Enable verbose output
-e, --endpoint URL  The HDF Server endpoint, e.g. http://hsdshdflab.hdfgroup.org
-u, --user USERNAME  User name credential
-p, --password PSSWD  Password credential
-o OWNER  Username of the domain's owner
--logfile LOGFILE   Logfile path
--loglevel LEVEL
    Change log level, one of: ``debug``, ``info``, ``warning``, ``error``.
--bucket BUCKET  Storage bucket


hsdel
=====

Usage::

    hsdel [ OPTIONS ] DOMAINS

Delete one or more HDF Cloud domains.

Example::

    hsdel -e http://hsdshdflab.hdfgroup.org /hdfgroup/data/test/deleteme.h5

Arguments
---------

`DOMAINS`
    One or more HDF Cloud domains.

Options
-------

-h, --help  Help message
-v, --verbose   Enable verbose output
-e, --endpoint URL  The HDF Server endpoint, e.g. http://hsdshdflab.hdfgroup.org
-u, --user USERNAME  User name credential
-p, --password PSSWD  Password credential
--logfile LOGFILE   Logfile path
--loglevel LEVEL
    Change log level, one of: ``debug``, ``info``, ``warning``, ``error``.
--bucket BUCKET  Storage bucket


hscopy
======

Usage::

    hscopy [ OPTIONS ]  SOURCE  DESTINATION

Copy an HDF Cloud domain to another domain.

Arguments
---------

`SOURCE`
    HDF Cloud domain to be copied.
`DESTINATION`
    Target HDF Cloud domain.

Options
-------

-h, --help  Help message
-v, --verbose   Enable verbose output
-e, --endpoint URL  The HDF Server endpoint, e.g. http://hsdshdflab.hdfgroup.org
-u, --user USERNAME  User name credential
-p, --password PSSWD  Password credential
-c, --conf CFGFILE   Credential and configuration file
--cnf-eg  Print the config file and exit.
--logfile LOGFILE   Logfile path
--loglevel LEVEL
    Change log level, one of: ``debug``, ``info``, ``warning``, ``error``.
--bucket BUCKET  Storage bucket
--src_bucket BUCKET  Storage bucket of the source domain.
--des_bucket BUCKET  Storage bucket for the destination domain.
--nodata  Do not copy dataset data.


hsmv
====

Usage::

    hsmv [ OPTIONS ]  SOURCE_DOMAIN  DEST_DOMAIN
    hsmv [ OPTIONS ]  SOURCE_DOMAIN  FOLDER

Move an HDF Cloud domain from one location to another.

Examples::

    hsmv /home/myfolder/file1.h5  /home/myfolder/file2.h5
    hsmv /home/myfolder/file1.h5  /home/myfolder2/

Arguments
---------

`SOURCE_DOMAIN`
    HDF Cloud domain to be moved.
`DEST_DOMAIN`
    Destination HDF Cloud domain.
`FOLDER`
    Destination HDF Cloud folder (UNIX style ending in ``/``).

Options
-------

-h, --help  Help message
-v, --verbose   Enable verbose output
-e, --endpoint URL  The HDF Server endpoint, e.g. http://hsdshdflab.hdfgroup.org
-u, --user USERNAME  User name credential
-p, --password PSSWD  Password credential
-c, --conf CFGFILE   Credential and configuration file
--cnf-eg  Print the config file and exit.
--logfile LOGFILE   Logfile path
--loglevel LEVEL
    Change log level, one of: ``debug``, ``info``, ``warning``, ``error``.
--bucket BUCKET  Storage bucket


hsdiff
======

Usage::

    hsdiff [ OPTIONS ]  FILE  DOMAIN

Compate an HDF5 file with a domain.

Arguments
---------

`FILE`
    HDF5 file.
`DOMAIN`
    HDF Cloud domain.

Options
-------

-h, --help  Help message
-v, --verbose   Enable verbose output
-e, --endpoint URL  The HDF Server endpoint, e.g. http://hsdshdflab.hdfgroup.org
-u, --user USERNAME  User name credential
-p, --password PSSWD  Password credential
-c, --conf CFGFILE   Credential and configuration file
--cnf-eg  Print the config file and exit.
--logfile LOGFILE   Logfile path
--loglevel LEVEL
    Change log level, one of: ``debug``, ``info``, ``warning``, ``error``.
--bucket BUCKET  Storage bucket
--nodata  Do not compare dataset data.
--noattr  Do not compare attributes.
--quiet  Do not produce output.


.. _hsacl:

hsacl
=====

Usage::

    hsacl [ OPTIONS ] DOMAIN +-CRUDEP [userid1 userid2 ...]

Examples
--------

* List ACLs::

    hsacl /home/jill/myfile.h5

* List user ``ted``'s ACLs::

    hsacl /home/jill/myfile.h5 ted

* Add/update ACL to give user ``ted`` read and update permissions::

    hsacl /home/jill/myfile.h5 +ru ted

* Remove all permissions except read for user ``jill``::

    hsacl /home/jill/myfile.h5 -cudep jill

Arguments
---------

`DOMAIN`
    A domain or folder to be updated.
`+-CRUDEP`
    Add (`+`) or remove (`-`) permissions for:

    * create (`C` )
    * read (`R` )
    * update (`U` )
    * delete (`D` )
    * read ACL (`E` )
    * update ACL (`P` )

Options
-------

-h, --help  Help message
-v, --verbose   Enable verbose output
-e, --endpoint URL  The HDF Server endpoint, e.g. http://hsdshdflab.hdfgroup.org
-u, --user USERNAME  User name credential
-p, --password PSSWD  Password credential
--logfile LOGFILE   Logfile path
--loglevel LEVEL
    Change log level, one of: ``debug``, ``info``, ``warning``, ``error``.
--bucket BUCKET  Storage bucket

hsget
=====

Usage::

    hsget [ OPTIONS ]  DOMAIN FILEPATH

Copy server domain to local HDF5 file.

Arguments
---------

`DOMAIN`
    HDF Cloud domain (UNIX or DNS style)
`FILEPATH`
    HDF5 file to be created

Options
-------

-h, --help  Help message
-v, --verbose   Enable verbose output
-e, --endpoint URL  The HDF Server endpoint, e.g. http://hsdshdflab.hdfgroup.org
-u, --user USERNAME  User name credential
-p, --password PSSWD  Password credential
-c, --conf CFGFILE   Credential and configuration file
--cnf-eg  Print the config file and exit.
--nodata   Do not download dataset data
--logfile LOGFILE   Logfile path
--loglevel LEVEL
    Change log level, one of: ``debug``, ``info``, ``warning``, ``error``.
--bucket BUCKET  Storage bucket

.. _hsconfigure:

hsconfigure
===========

Usage::

    hsconfigure

Interactive editing of the user HDF Cloud configuration.
