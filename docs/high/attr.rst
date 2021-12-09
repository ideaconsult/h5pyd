.. currentmodule:: h5pyd
.. _attributes:


Attributes
==========

Attributes are a critical part of what makes HDF5 a self-describing
format. They are small named pieces of data assigned directly to
:class:`Group` and :class:`Dataset` objects.  This is the official way to
store metadata in HDF5.

Each Group or Dataset has a small proxy object attached to it, available from the ``.attrs`` property. Attributes have the following properties:

- They may be created from any scalar or NumPy array
- There is no chunked I/O (i.e. slicing); the entire attribute is read and written in one operation.

The ``.attrs`` proxy objects are of class :class:`AttributeManager`, below.
This class supports a dictionary-style interface.


Reference
---------

.. class:: AttributeManager(parent)

    AttributeManager objects are created directly for a group or dataset. No
    need to create them manually.

    .. method:: __iter__()

        Get an iterator over attribute names.

    .. method:: __contains__(name)

        Determine if attribute `name` to this object exists.

    .. method:: __getitem__(name)

        Retrieve an attribute.

    .. method:: __setitem__(name, val)

        Create an attribute, overwriting any existing attribute with the same
        ``name``. The type and shape of the attribute are determined
        automatically by h5pyd based on ``val``.

    .. method:: __delitem__(name)

        Delete an attribute. ``KeyError`` if it doesn't exist.

    .. method:: __len__()

        Number of attributes.

    .. method:: keys()

        Get the names of all attributes assigned to this object.

        :return: set-like object.

    .. method:: values()

        Get the values of all attributes assigned to this object.

        :return: collection or bag-like object.

    .. method:: items()

        Get ``(name, value)`` tuples for all attributes assigned to this object.

        :return: collection or set-like object.

    .. method:: get(name, default=None)

        Retrieve attribute `name`'s value or `default` if no such attribute
        exists.

    .. method:: create(name, data, shape=None, dtype=None)

        Create a new attribute, with control over the shape and type.  Any
        existing attribute will be overwritten.

        :param name:    Name of the new attribute
        :type name:     :class:`str`

        :param data:    Value of the attribute; will be put through
                        ``numpy.array(data)``.

        :param shape:   Shape of the attribute.  Overrides ``data.shape`` if
                        both are given, in which case the total number of
                        points must be unchanged.
        :type shape:    :class:`tuple`

        :param dtype:   Data type for the attribute.  Overrides ``data.dtype``
                        if both are given.
        :type dtype:    :class:`numpy.dtype`


    .. method:: modify(name, value)

        Change the value of an attribute while preserving its type and shape.
        Unlike :meth:`AttributeManager.__setitem__`, if the attribute already
        exists only its value will be changed.

        If the attribute doesn't exist, it will be created with a default
        shape and type.

        :param name:    Name of attribute to modify.
        :type name:     :class:`str`

        :param value:   New value.  Will be put through ``numpy.array(value)``.
