*****
Table
*****

Reference
=========

.. currentmodule:: h5pyd

.. class:: Table(dsetid)

    Tabular data interface for one-dimensional HDF5 datasets.

    :param dsetid: DatasetID instance of an h5pyd dataset.

    .. method:: read(start=None, stop=None, step=None, field=None, out=None)

        .. todo:: Missing method description.

    .. method:: read_where(condition, condvars=None, field=None, start=None, stop=None, step=None, limit=None)

        Read rows (dataset elements) that satify a PyTable-style `condition`.

    .. method:: update_where(condition, value, start=None, stop=None, step=None, limit=None)

        Modify rows (dataset elements) that satify a PyTable-style `condition`.

    .. method:: create_cursor(condition=None,  start=None, stop=None)

        Return a :class:`h5pyd._hl.table.Cursor` instance to iterate over the selected rows.

    .. method:: append(rows)

        Append `rows` to the end of the table (dataset).

    .. attribute:: colnames

        A list with compound datatype field names.

    .. attribute:: nrows

        Number of rows (elements of the dataset).


.. currentmodule:: h5pyd._hl.table

.. class:: Cursor(table, query=None, start=None, stop=None, buffer_rows=None)

    A Cursor instance for retrieving selected table rows.

    :param table: An :class:`h5pyd.Table` instance.
    :param query: A query condition to select table rows.
    :param start: Start row index.
    :type start: int
    :param stop: Stop row index.
    :type stop: int
    :param buffer_rows: Control how many rows to fetch from the server in one operation.

    .. method:: __iter__()

        Iterate of table rows.

        .. caution:: Modifications to the yielded data are **not** written to file.
