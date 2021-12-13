.. currentmodule:: h5pyd
.. _file:


File Objects
============

File objects serve as your entry point into the world of HDF5.  In addition
to the File-specific capabilities listed here, every File instance is
also an :ref:`HDF5 group <group>` representing the `root group` of the file.

.. _file_open:

Opening & creating files
------------------------

HDF5 file objects work generally like standard Python file objects.  They support
standard modes like r/w/a, and should be closed when they are no longer in
use.  However, there is obviously no concept of "text" vs "binary" mode.

    >>> f = h5pyd.File('/home/myhome/myfile.hdf5','r')

The file path may be a byte string or unicode string. The path must start with a '/' (absolute path).
Valid modes are:

========  ================================================
    r        Readonly, file object must exist (default)
    r+       Read/write, file object must exist
    w        Create file object, reset if exists
w- or x      Create file object, fail if exists
    a        Read/write if exists, create otherwise
========  ================================================

The file path do not correspond directly to posix file path, but is a resource location
relative to the parent path and ultimately to a storage location that is managed by the server.
If the folder resource referenced by the parent path does not exist, an error will be raised.

.. versionchanged:: 0.8.0
   Files are now opened read-only by default. Earlier versions of h5pyd would
   pick different modes depending on the presence and permissions of the file.


.. _authentication:

Authentication
--------------

Typically the server will be configured to verify the identity of the requestor
- either by the requestor supplying a username/password combination (HTTP Basic
Auth) or an OAuth-based bearer token.  If the identity of the requestor cannot be
determined, a ``401 - Unauthorized`` error will be raised.

For username/password based authentication, there are three different means to supplying
the credentials:

1. Provide username and password parameters in the File initialization.
2. Set the HS_USERNAME and HS_PASSWORD environment variables
3. Set hs_username and hs_password keys in a file ".hscfg" in the client's home directory.

Using username and password in the file parameters overrides the environment variables or
hscfg entries.  The :ref:`hsconfigure` app can be used to create/update the .hscfg file.

Note: In "direct" mode, the username is not validated, but the username is still used for
for the authorization check.  See: :ref:`authorization`.

.. _authorization:

Authorization
-------------

Even after the server has validated the supplied credentials, it may still be the case that
the requesting user does not have permissions to open the file object in the give mode.
Each file and folder resource on the server maintains a set of "Access Control Lists" (ACLs)
that define what actions can be performed by a given user.

Each ACL is a dictionary with the following keys:

userName
    user that the ACL is associated with or "default"
create
    create operations allowed (e.g. create new dataset)
read
    ead operation allowed (e.g. read value from dataset)
update
    update operations allowed (e.g. modify dataset value)
delete
    delete operations allowed (e.g. delete a link)
readACL
    the ACLs  can be read
updateACL
    ACLs can be modified

If no ACL is found for the given username that supports the requested mode, but an ACL
with the username 'default' exists, the default ACL is used.

If no ACL is found, a ``403-Forbidden`` error is raised.

if an ACL is found, the operation is permitted if the corresponding ACL property is True,
otherwise a ``403-Forbidden`` error is raised.

For 'w' and 'a' modes, the parent folder must have an ACL with 'create' mode enabled.

Finally, if the username is an admin user (as configured on the server), an action is allowed
(assuming the user's credentials are valid).

The :ref:`hsacl` tool can be used to read and update acls.


.. _concurrent:

Concurrent Access
-----------------

It's possible for multiple clients to read and write to the same file resource simultaneously.
The server enable storage to be updated in a consistent manner and no explict synchronization
is needed on part of the clients.  Care should be taken though that multiple clients don't attempt
update the same attribute, or modify the same dataset values, without some means of coordination as the result will
based on the last request to be processed by the server.

Asynchronous properties
-----------------------

A number of file object properties are updated asynchrounously by the server.
Since the server may be a distributed system, and the amount of state for a given file
can be arbitrary large, a property such as "num_objects" cannot be
efficiently determined per request.  Instead the set of objects within a file are scanned
periodically by the server and stored for future requests. When a async property is read,
the value as of the last scan is returned.

Example:

.. code-block:: python

   f = h5pyd.File(a_file_path, 'w+')
   ts = f.last_scan
   f.create_group("a_new_group")
   while f.last_scan == ts:
       time.sleep(1) # wait for the server to re-scan file
   print(f.num_objects)  # number of objects updated

The asynchonous properties of the file object are labeled "async" below.

.. _endpoint:

Endpoint
--------

The endpoint is used to specify the url for h5pyd to send http requests to.  Typically,
the endpoint consist of URL giving the protocal (http or https), the dns name or IP address
of the server, and the port number.  For example: http://127.0.0.1:5101 for a server running
on the local machine access through port 5191.

There are two special endpoints that are used for serverless access:

The endpoint "local[*]" can be used for "direct" mode where server subprocesses are
created on the local machine.  when the file is opened.  See "direct access" TBD.

The endpoint "hslambda" can be used to invoke AWS Lambda implementation.  See "hslambda" TBD.


Unsupported Featues
-------------------

The following h5py parameters are not supported by h5pyd (generally because they
are not relevant):

================  ======================================================
driver             no equivalent in h5pyd
libver             HDF5 library is not used by h5pyd
userblock_size     userblock not supported
swmr               No single-writer-multiple-reader mode.  See :ref   _concurrent.
rdcc_nybtes        No client-side chunk cache
rdcc_w0            Chunk preemption controlled by server
rdcc_nslots        No client-side chunk cache
track_order        creation order is always tracked by server
fs_strategy        Not relevant
fs_persist         Not relevent
fs_threshold       Not relevant
kwds               No driver for h5pyd, so no driver-specific keywords
================  ======================================================


.. _file_closing:

Closing files
-------------

If you call :meth:`File.close`, or leave a ``with h5pyd.File(...)`` block,
the file object will be closed and the file object will become unusable.  The
connection to the server will only be closed by any object (dataset, group, etc) that
refrences the object is out of scope.


.. code-block:: python

    with h5pyd.File('/shared/tall.h5') as f1:
        ds = f1['/g1/g1.1/dset.1.1']

    ds[0]  # OK - ds still maintains a connection to the server

    del ds  # Now the server connection will be closed

.. _file_filenames:

Filenames on different systems
------------------------------

Different operating systems (and different file systems) store filenames with
different encodings. Additionally, in Python there are at least two different
representations of filenames, as encoded ``bytes`` or as a Unicode string
(``str`` on Python 3).

h5pyd always return filenames as ``str``, e.g.
:attr:`File.filename`. h5pyd accepts filenames as either ``str`` or ``bytes``.
In most cases, using Unicode (``str``) paths is preferred.

Unlike with h5py, there are no OS-dependent differences.

.. _file_cache:

Chunk cache
-----------

:ref:`dataset_chunks` are used as a means of storing datasets separate pieces.
When a part of any one of these pieces is needed, the entire chunk is read into
on the server before the requested part is sent to the client.  To the extent
possible those chunks are cached in memory, so that if a client requests a
different part of a chunk that has already been read, the data can be copied
directly from memory rather than reading from storage again.  The details of a
given dataset's chunks are controlled when creating the dataset.  The size of
the chunk cache depends on the server configuration, see the server documentatin
for details.

Currently, h5pyd does not provide any local cache for chunk data.  Typically,
it will be more effience to read relatively large portions of the dataset than
to make many smaller requests to the server.

Reference
---------

.. class:: File(name, mode=None, endpoint=None, username=None, \
    password=None, bucket=None, api_key=None, use_session=True, \
    use_cache=True, use_shared_memr=None, owner=None, linked_domain=None, \
    retries=10, **kwds)

    Open or create a new file.

    Note that in addition to the File-specific methods and properties listed
    below, File objects inherit the full interface of :class:`Group`.

    :param name:    Path to file object resource.  Must start with '/'.
    :param mode:    Mode in which to open file; one of
                    ("w", "r", "r+", "a", "w-").  See :ref:`file_open`.
    :param endpoint:  Endpoint to be used; see :ref:`endpoint`.
    :param username:  Username; see :ref:`authentication`.
    :param password:  Password for given user; see :ref:`authentication`
    :param bucket: Storage collection (e.g. AWS S3 bucket or Azure container) to be used.  If not provided the
                default configured on the server will be used.
    :param api_key: Api Key to be used in lieu of username/password; see :ref:`authentication`
    :param use_session: Maintain an http connection as long as the file object
                    is open.  Default to True.
    :param use_cache: Cache metadata (links, attributes, dataset shape, etc.) so a new
           server request is not needed each time an object is accesed.  Default is True.
           Use False if it's expected that value maybe changed by another client while
           the file object is opened.  See :ref:`concurrent` for more information.
    :param use_shared_mem: Use shared memory to pass dat rather than http.
            Only supported when the server is on the same machine as client.  Default to False.
    :param logger: Use provided logger for log messages.  Default to None.
    :param owner: Assign the given value as owner for a new file object (rather than username).
            Requires that username be an admin user.
    :param linked_domain: Create a new file object using the same root as the
            file object referenced by 'linked_domain'.  Basically creats an alias for the
            same HDF root group.
    :param retries: If a request to the server fails (for instance the server is temporarily
            too busy to handle the request), retry the request by the given number of times.
    :param kwds:  Additional parameters.  TBD

    .. method:: __bool__()

        Check that the file descriptor is valid and the file open:

            >>> f = h5pyd.File(filename)
            >>> f.close()
            >>> if f:
            ...     print("file is open")
            ... else:
            ...     print("file is closed")
            file is closed

    .. method:: close()

        Close this file.  File object will become invalid.

    .. method:: flush()

        Request that the server write all modified objects to storage.

    .. attribute:: id

        Low-level identifier (an instance of :class:`GroupID`).

    .. attribute:: filename

        Name of this file object, as a Unicode string.

    .. attribute:: mode

        String indicating if the file is open readonly ("r") or read-write
        ("r+").  Will always be one of these two values, regardless of the
        mode used to open the file.

    .. attribute:: modified

        Timestamp of the most recently modified object in the file object.
        May take a few seconds to be updated after an object has been updated.

    .. attribute:: num_objects

        Number of objects (groups, datasets, or committed types) in the file object. (async)

    .. attribute:: num_datatypes

        Number of committed datatype objects. (async)

    .. attribute:: num_groups

        Number of group objectsk. (async)

    .. attribute: num_chunks

        Number of chunks (over all datasets). (async)

    .. attribute: num_linked_chunks

        Number of chunks stored in HDF5 files (see linked files TBD). (async)

    .. attribute: num_datasets

        Number of datasets. (async)

    .. attribute: metadata_bytes

        Number of bytes used for metadata storage. (async)

    .. attribute: linked_bytes

        Number of bytes used in linked chunks. (async)

    .. attribute: total_size

        Total number of storage bytes used. (async)

    .. attribute: md5_sum

        MD5 checksum for the file object (will change whenever any data or metadata
        is modified). (async)

    .. attribute: last_scan

        Timestamp of the last time asynchronous properties were updates (see :ref: _async_props)

    .. attribute: compressors

        Return list of compressors supported by this server

    .. method: getACLs()

       Return a list of all ACLs for this file object.

    .. method: getACL(username)

       Return the ACL for the given username.  Raises a 404-Not Found error if no ACL for
       the given user exists.

    .. method: putACL(acl)

       Create a new ACL or modify an existing ACL for the fileobject.  See :ref: _authorization
       for a description of the acl.
