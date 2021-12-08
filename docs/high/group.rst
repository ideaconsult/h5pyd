.. currentmodule:: h5pyd
.. _group:

Groups
======

Groups provide the mechanism by which HDF5 file content is hierarchically
organized. From a Python perspective, they operate somewhat like dictionaries.
In this case the "keys" are the names of group members, and the "values" are the
members themselves (:class:`Group` and :class:`Dataset`) objects.

Group objects also contain most of the machinery which makes HDF5 useful.
The :ref:`File object <file>` does double duty as the HDF5 *root group*, and
serves as your entry point into the file:

    >>> f = h5pyd.File('/home/myhome/foo.hdf5','w')
    >>> f.name
    '/'
    >>> list(f.keys())
    []

Names of all objects in the file are text strings (``str``).


.. _group_create:

Creating groups
---------------

New groups are easy to create::

    >>> grp = f.create_group("bar")
    >>> grp.name
    '/bar'
    >>> subgrp = grp.create_group("baz")
    >>> subgrp.name
    '/bar/baz'

Multiple intermediate groups can also be created implicitly::

    >>> grp2 = f.create_group("/some/long/path")
    >>> grp2.name
    '/some/long/path'
    >>> grp3 = f['/some/long']
    >>> grp3.name
    '/some/long'


.. _group_links:

Dict interface and links
------------------------

h5pyd groups implement a subset of the Python dictionary convention.  They have
methods like ``keys()`` and ``values()``, and support iteration.  Most importantly,
they support the indexing syntax with standard exceptions:

    >>> myds = subgrp["MyDS"]
    >>> missing = subgrp["missing"]
    KeyError: "Name doesn't exist (Symbol table: Object not found)"

.. todo::  Check the KeyError exception!

Objects can be deleted from the file using the standard syntax::

    >>> del subgroup["MyDataset"]

.. note::
    In Python 3, the :meth:`Group.keys()`, :meth:`Group.values()` and :meth:`Group.items()` methods
    will return view-like objects instead of lists.  These objects support
    membership testing and iteration, but can't be sliced like lists.


.. _group_hardlinks:

Hard links
~~~~~~~~~~

What happens when assigning an HDF5 object to a name in the group?  It depends on
the type of object being assigned.  For NumPy arrays or other data, the default
is to create an :ref:`HDF5 dataset <dataset>`::

    >>> grp["name"] = 42
    >>> out = grp["name"]
    >>> out
    <HDF5 dataset "name": shape (), type "<i8">

When the object being stored is an existing Group or Dataset, a new link is
made to the object::

    >>> grp["other name"] = out
    >>> grp["other name"]
    <HDF5 dataset "other name": shape (), type "<i8">

Note that this is *not* a copy of the dataset!  Like hard links in a UNIX file
system, objects in an HDF5 file can be stored in multiple groups::

    >>> grp["other name"] == grp["name"]
    True


.. _group_softlinks:

Soft links
~~~~~~~~~~

Also like a UNIX filesystem, HDF5 groups can contain "soft" or symbolic links,
which contain a text path instead of a pointer to the object itself.  You
can easily create these in h5pyd with :class:`h5pyd.SoftLink`::

    >>> myfile = h5pyd.File('foo.hdf5','w')
    >>> group = myfile.create_group("somegroup")
    >>> myfile["alias"] = h5pyd.SoftLink('/somegroup')

If the target is removed, they will "dangle":

    >>> del myfile['somegroup']
    >>> print(myfile['alias'])
    KeyError: 'Component not found (Symbol table: Object not found)'

.. todo:: Verify KeyError message.

.. _group_extlinks:

External links
~~~~~~~~~~~~~~

External links are soft links that target an HDF5 object in another file, hence,
they require both the file name and the path to the target object in that file.
They have similar syntax as soft links:

    >>> myfile = h5pyd.File('/home/myhome/foo.hdf5', 'w')
    >>> myfile['ext link'] = h5pyd.ExternalLink("/home/myhome/otherfile.hdf5", "/path/to/resource")

When the external link is accessed, the file "/home/myhome/otherfile.hdf5" is
opened and the HDF5 object at "/path/to/resource" is returned. Since the object
retrieved is in a different file, its ``.file`` and ``.parent`` properties will
refer to objects in that file, *not* the file in which the link resides.

Reference
---------

.. class:: Group(identifier)

    Generally Group objects are created by opening objects in the file, or
    by the method :meth:`Group.create_group`.  Call the constructor with
    a :class:`GroupID <h5pyd.objectid.GroupID>` instance to create a new Group
    bound to an existing low-level identifier.

    .. method:: __iter__()

        Iterate over the names of the group's member objects (directly linked
        to it). Use :meth:`Group.visit` or :meth:`Group.visititems` for
        recursive access to all the objects accessible from this group.

    .. method:: __contains__(name)

        Dict-like membership testing.  `name` may be a relative or absolute
        path.

    .. method:: __getitem__(name)

        Retrieve an object.  `name` may be a relative or absolute path, or
        an :ref:`object or region reference <refs>`. See :ref:`group_links`.

    .. method:: __setitem__(name, value)

        Create a new link, or automatically create a dataset.
        See :ref:`group_links`.

    .. method:: __bool__()

        Check that the group is accessible.
        A group could be inaccessible for several reasons. For instance, the
        group, or the file it belongs to, may have been closed elsewhere.

        >>> f = h5pyd.open("/home/myhome/file.h5")
        >>> group = f["MyGroup"]
        >>> f.close()
        >>> if group:
        ...     print("group is accessible")
        ... else:
        ...     print("group is inaccessible")
        group is inaccessible

    .. method:: keys()

        Get the names of directly attached group members. Use
        :meth:`Group.visit` or :meth:`Group.visititems` for recursive access to
        all objects accessible from this group.

       :return: set-like object.

    .. method:: values()

        Get the objects contained in the group (Group and Dataset instances).
        Broken soft or external links show up as None.

        :return: a collection or bag-like object.

    .. method:: items()

        Get ``(name, object)`` pairs for objects linked to this group.
        Values for broken soft or external links show up as None.

        :return: a set-like object.

    .. method:: get(name, default=None, getclass=False, getlink=False)

        Retrieve an object, or information about an object.  `name` and
        `default` work like the standard Python ``dict.get()``.

        :param name: Name of the object to retrieve.  May be a relative or
                     absolute path.
        :param default: If the object isn't found, return this instead.
        :param getclass: If True, return the class of object instead;
                         :class:`Group` or :class:`Dataset`.
        :param getlink: If true, return the type of link via a :class:`HardLink`,
                        :class:`SoftLink` or :class:`ExternalLink` instance.
                        Return "default" if nothing with that name exists.

    .. method:: visit(callable)

        Recursively visit all objects in this group and its subgroups.  You supply
        a callable with the signature::

            callable(name) -> None or return value

        `name` will be the name of the object relative to the current group.
        Return ``None`` to continue visiting until all objects are exhausted.
        Returning anything else will immediately stop visiting and return
        that value from ``visit``::

            >>> def find_foo(name):
            ...     """ Find first object with 'foo' anywhere in the name """
            ...     if 'foo' in name:
            ...         return name
            >>> group.visit(find_foo)
            'some/subgroup/foo'

    .. method:: visititems(callable)

        Recursively visit all objects in this group and its subgroups. Like
        :meth:`Group.visit`, except your callable should have the signature::

            callable(name, h5obj) -> None or return value

        In this case `h5obj` will be a :class:`Group` or :class:`Dataset`
        instance.


    .. .. method:: move(source, dest)

    ..     Move an object or link in the file.  If `source` is a hard link, this
    ..     effectively renames the object.  If a soft or external link, the
    ..     link itself is moved.

    ..     :param source:  Name of object or link to move.
    ..     :type source:   String
    ..     :param dest:    New location for object or link.
    ..     :type dest:   String


    .. .. method:: copy(source, dest, name=None, shallow=False, expand_soft=False, expand_external=False, expand_refs=False, without_attrs=False)

    ..     Copy an object or group.  The source and destination need not be in
    ..     the same file.  If the source is a Group object, by default all objects
    ..     within that group will be copied recursively.

    ..     :param source:  What to copy.  May be a path in the file or a Group/Dataset object.
    ..     :param dest:    Where to copy it.  May be a path or Group object.
    ..     :param name:    If the destination is a Group object, use this for the
    ..                     name of the copied object (default is basename).
    ..     :param shallow: Only copy immediate members of a group.
    ..     :param expand_soft: Expand soft links into new objects.
    ..     :param expand_external: Expand external links into new objects.
    ..     :param expand_refs: Copy objects which are pointed to by references.
    ..     :param without_attrs:   Copy object(s) without copying HDF5 attributes.


    .. method:: create_group(name)

        Create and return a new group.

        :param name:    Name of group to create.  May be an absolute
                        or relative path. Fails if an object with the name
                        already exists. Provide ``None`` to create an anonymous
                        group, to be linked into the file later.
        :type name:     :class:`str` or ``None``

        :return:        The new :class:`Group` object.


    .. method:: require_group(name)

        Open a group in the file, creating it if it doesn't exist.
        ``TypeError`` is raised if a conflicting object already exists.
        Parameters as in :meth:`Group.create_group`.


    .. method:: create_dataset(name, shape=None, dtype=None, data=None, **kwds)

        Create a new dataset.  Options are explained in :ref:`dataset_create`.

        :param name:    Name of dataset to create.  May be an absolute
                        or relative path.  Provide ``None`` to create an anonymous
                        dataset, to be linked into the file later.

        :param shape:   Shape of new dataset as a tuple. Use ``()`` for scalar
                        datasets.  Required if `data` isn't provided.

        :param dtype:   Numpy dtype or string. If omitted, ``dtype('f')`` will be used.
                        Required if "data" isn't provided; otherwise, overrides data
                        array's dtype.

        :param data:    Initialize dataset to this (NumPy array). Can omit
                        `shape` and `dtype` arguments if used.

        Keyword-only arguments:

        :keyword chunks:    Chunk shape as a tuple, or ``True`` to enable
                            auto-chunking.
        :type chunks: :class:`tuple`

        :keyword maxshape:  Dataset will be resizable up to this shape.
                            Automatically enables chunking.  Use ``None`` for the
                            dimensions you want to be unlimited.
        :type maxshape: :class:`tuple` or ``None``

        :keyword compression:   Compression strategy.  See :ref:`dataset_compression`.

        :keyword compression_opts:  Parameters for compression filter. See :ref:`dataset_compression`.

        :keyword scaleoffset:   See :ref:`dataset_scaleoffset`.

        :keyword shuffle:   Enable shuffle filter. See :ref:`dataset_shuffle`.

        :keyword fillvalue: A scalar value that provided for every uninitialized
                            dataset element.

        :keyword track_times: Enable dataset creation timestamps. ``True``
                              (default) or ``False``.


    .. method:: require_dataset(name, shape=None, dtype=None, exact=False, **kwds)

        Open a dataset, creating it if it doesn't exist.

        If keyword "exact" is ``False`` (default), an existing dataset must have
        the same shape and a conversion-compatible dtype to be returned.  If
        ``True``, the shape and dtype must match exactly.

        Other dataset keywords (see :meth:`create_dataset`) may be provided, but are
        only used if a new dataset is to be created.

        Raises ``TypeError`` if an incompatible object already exists, or if the
        shape or dtype don't match according to the above rules.

        :keyword exact: Require shape and type to match exactly (T/**F**)


    .. method:: create_dataset_like(name, other, **kwds)

        Create a dataset similar to `other`.

        :param name:
            Name of the dataset (absolute or relative).  Provide ``None`` to make
            an anonymous dataset.
        :type name: str or ``None``
        :param other:
            The dataset whom the new dataset should mimic. All properties, such
            as shape, dtype, chunking, ... will be taken from it, but no data
            or attributes are being copied.
        :type other: :class:`Dataset`

        Any dataset keywords (see :meth:`create_dataset`) may be provided, including
        `shape` and `dtype`, in which case the provided values take precedence over
        those from `other`.

    .. attribute:: attrs

        :ref:`attributes` for this group.

    .. attribute:: id

        The groups's low-level identifier; an instance of
        :class:`GroupID <h5pyd.objectid.GroupID>`.

    .. attribute:: ref

        An HDF5 object reference pointing to this group.  See
        :ref:`refs_object`.

    .. .. attribute:: regionref

    ..     A proxy object allowing you to interrogate region references.
    ..     See :ref:`refs_region`.

    .. attribute:: name

        String giving the full path to this group.

    .. attribute:: file

        :class:`File` instance in which this group resides.

    .. attribute:: parent

        :class:`Group` instance containing this group.

    .. attribute:: modified

        Last modified time as a `datetime.datetime` object.


Link classes
------------

.. class:: HardLink()

    Exists only to support :meth:`Group.get`.  Has no state and provides no
    properties or methods.

.. class:: SoftLink(path)

    Exists to allow creation of soft links in the file.
    See :ref:`group_softlinks`.  These only serve as containers for a path;
    they are not related in any way to a particular file.

    :param path:    Value of the soft link.
    :type path:     :class:`str`

    .. attribute:: path

        Value of the soft link

.. class:: ExternalLink(filename, path)

    Like :class:`SoftLink`, only they specify a filename in addition to a
    path.  See :ref:`group_extlinks`.

    :param filename:    Name of the file to which the link points
    :type filename:     :class:`str`

    :param path:        Path to the object in the external file.
    :type path:         :class:`str`

    .. attribute:: filename

        Name of the external file as a Unicode string

    .. attribute::  path

        Path to the object in the external file
