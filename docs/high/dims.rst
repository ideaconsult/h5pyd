.. currentmodule:: h5pyd._hl.dims

.. _dimension_scales:

Dimension Scales
================

Datasets are multidimensional arrays. HDF5 provides support for labeling the
dimensions and associating one or more *dimension scales* with each dimension. A
dimension scale is just another HDF5 dataset. In principle, a dimension scale
should be a one-dimensional HDF5 dataset with that dimension's size matching the
multidimensional array's dimension of interest. However, this is not a data
model requirement nor is enforced by HDF software.

Dimension scales are very useful for scientific or engineering data where it is important to also provide `coordinate data`. For example, let's consider an instrument measuring some physical property over time. Those instrument data would be stored as an HDF5 dataset. But, how to store the times when each of those measurements were made? The best option, from the data management perspective, is to store the measurement time in another HDF5 dataset, make it a dimension scale, and attach it to the first dimension of the instrument data's HDF5 dataset. Both data are kept separate which makes it easier to provide further metadata, such as physical units, instrument information, etc.

H5pyd provides dimension scale interface through the :attr:`h5pyd.Dataset.dims`
property. Suppose we have the following data file:

.. code-block:: python

    f = h5pyd.File('/home/myhome/foo.h5', 'w')
    f['data'] = np.ones((4, 3, 2), 'f')

The dimensions of the ``data`` dataset can be labeled, for example::

    f['data'].dims[0].label = 'z'
    f['data'].dims[2].label = 'x'

Note that the first dimension, which has a size of 4, has been labeled "z",
the third dimension (in this case the fastest varying dimension), has been
labeled "x", and the second dimension was given no label at all.

We can also use HDF5 datasets as dimension scales. For example, if we have::

    f['x1'] = [1, 2]
    f['x2'] = [1, 1.1]
    f['y1'] = [0, 1, 2]
    f['z1'] = [0, 1, 4, 9]

We are going to treat the ``x1``, ``x2``, ``y1``, and ``z1`` datasets as
dimension scales::

    f['x1'].make_scale()
    f['x2'].make_scale('x2 name')
    f['y1'].make_scale('y1 name')
    f['z1'].make_scale('z1 name')

When you create a dimension scale, you may provide a name for that scale. In
this case, the ``x1`` scale was not given a name, but the others were. Now we
can associate these dimension scales with the primary dataset::

    f['data'].dims[0].attach_scale(f['z1'])
    f['data'].dims[1].attach_scale(f['y1'])
    f['data'].dims[2].attach_scale(f['x1'])
    f['data'].dims[2].attach_scale(f['x2'])

Note that two dimension scales, ``x1`` and ``x2``, were associated with the
third dimension of ``data``. You can also detach a dimension scale::

    f['data'].dims[2].detach_scale(f['x2'])

but for now, lets assume that we have both ``x1`` and ``x2`` still associated
with the third dimension of ``data``. You can attach a dimension scale to any
number of HDF5 datasets, you can even attach it to multiple dimensions of the
same HDF5 dataset.

Now that the dimensions of ``data`` have been labeled, and the dimension scales
for the various axes have been specified, we have provided much more context
with which ``data`` can be interpreted. For example, if you want to know the
labels for the various dimensions of ``data``::

    >>> [dim.label for dim in f['data'].dims]
    ['z', '', 'x']

If you want the names of the dimension scales associated with the "x" dimension::

    >>> f['data'].dims[2].keys()
    ['', 'x2 name']

:meth:`items` and :meth:`values` methods are also provided. The dimension
scales themselves can also be accessed with::

    f['data'].dims[2][1]

or::

    f['data'].dims[2]['x2 name']

such that::

    >>> f['data'].dims[2][1] == f['x2']
    True

though, beware that if you attempt to index the dimension scales with a string,
the first dimension scale whose name matches the string is the one that will be
returned. There is no guarantee that the name of the dimension scale is unique.

Nested dimension scales are not permitted: if a dataset has a dimension scale
attached to it, converting the dataset to a dimension scale will fail, since the
`HDF5 Dimension Scale specification
<https://support.hdfgroup.org/HDF5/doc/HL/H5DS_Spec.pdf>`_ doesn't allow this.::

   >>> f['data'].make_scale()
   RuntimeError: Unspecified error in H5DSset_scale (return value <0)

Reference
---------

.. note::

    The following dimension scale API is not to be used directly but only via
    the :attr:`h5pyd.Dataset.dims` property.

.. class:: DimensionProxy(id, dimension)

    Represents one dimension of an HDF5 dataset.

    :param id: ``DatasetID`` instance of an HDF5 dataset.

    :param dimension: Dimension position. (0 for first dimension, 1 for second, etc.)
    :type dimension: Positive :class:`int`.

    .. method:: __getitem__(val)

        Get the dimension scale at `val`.

        `val` can be either an integer or a string representing a dimension scale name.

        :return: :class:`h5pyd.Dataset` instance of the dimension scale.

    .. method:: __iter__()

        Names of the dimension scales attached to this dimension.

        :return: A generator.

    .. method:: __len__()

        Number of dimension scales attached.

    .. method:: attach_scale(dscale)

        Attach a dimension scale to this dimension.

        :param dscale: Dimension scale to be attached.
        :type dscale: :class:`h5pyd.Dataset`

    .. method:: detach_scale(dscale)

        Detach (remove) a dimension scale from this dimension.

        :param dscale: Dimension scale to be removed.
        :type dscale: :class:`h5pyd.Dataset`

    .. method:: item()

        Get a list of (`name`, `dscale`) tuples with all dimension scales
        attached to this dimension.

        :return: a list of (:class:`str`, :class:`h5pyd.Dataset`) tuples

    .. method:: keys()

        A list with names of attached dimension scales.

    .. method:: values()

        A list of :class:`h5pyd.Dataset` instances of attached dimension scales.

    .. attribute:: label

        Dimension's label. An empty string if label is not set.

        To set a label use ``label(name)``.

.. class:: DimensionManager(dset)

    Represents all dimensions of one HDF5 dataset.

    :param dset: :class:`h5pyd.Dataset` instance

    .. method:: __len__()

        Number of HDF5 dimensions, i.e., dataset's rank.

    .. method:: __getitem__(index)

        Get a :class:`DimensionProxy` instance for dimension `index`.

    .. method:: __iter__()

        Iterate over :class:`DimensionProxy` instances of every dataset's dimension.

        :return: A generator.

    .. method:: create_scale(dset, name='')

        Make a dataset `dset` a dimension scale.

        :param dset: A dataset to become a dimension scale.
        :type dset: :class:`h5pyd.Dataset`

        :param name: Optional dimension scale name. Default is an empty string.
        :type name: :class:`str`

.. currentmodule:: h5pyd.h5ds

.. function:: is_scale(dsid)

    True if an HDF5 dataset is also a dimension scale.

    :param dsid: :class:`h5pyd._hl.objectid.DatasetID` instance of an HDF5 dataset.

    :return: :class:`bool` (``True`` or ``False``)

.. function:: is_attached(dsetid, dscaleid, idx)

    True if Dimension Scale ``dscale`` is attached to Dataset ``dset`` at dimension ``idx``.

    :param dsetid: :class:`h5pyd._hl.objectid.DatasetID` instance of the dataset
                    with attached dimension scales.

    :param dscaleid: :class:`h5pyd._hl.objectid.DatasetID` instance of a dimension scale.
