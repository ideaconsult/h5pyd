What is Different from h5py?
============================

.. warning::

    This is a collection place for all the h5py documentation that does not fit
    anywhere else for now.

.. toctree::
    :maxdepth: 1

    mpi
    vds
    high/lowlevel

From `group.rst`
----------------

By default, objects inside group are iterated in alphanumeric order.
However, if group is created with ``track_order=True``, the insertion
order for the group is remembered (tracked) in HDF5 file, and group
contents are iterated in that order.  The latter is consistent with
Python 3.7+ dictionaries.

The default ``track_order`` for all new groups can be specified
globally with ``h5.get_config().track_order``.

``h5pyd.Group.move()`` and ``h5pyd.Group.copy()`` not supported.

Fletcher32 filter is not supported.

No virtual dataset methods for the Group class.
