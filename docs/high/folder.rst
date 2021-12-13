.. currentmodule:: h5pyd

======
Folder
======

Reference
=========

.. class:: Folder(path, pattern=None, query=None, mode=None, endpoint=None, verbose=False, username=None, password=None, bucket=None, api_key=None, logger=None, owner=None, batch_size=1000, retries=3, **kwds)

    Represent an HDF Cloud folder with domains.

    :param path: Folder path.
    :param pattern: Regex filter to apply on the folder's domains.
    :param query: Query for domain root level attributes. Only the domains that match will be included.
    :param mode: Folder access mode. One of: ``r``, ``r+``, ``w``, ``a``.
    :param endpoint: Server endpoint. Default: `http://localhost:5000`.
    :param username: User name.
    :param password: User's password.
    :param bucket: Bucket or storage container to use. If not set, server default bucket will be used.
    :param api_key: User's API key. An alternative to `username`/`password` for authentication.
    :param logger: Log handler to use.
    :param owner: The owner for any new domains created in the folder. Defaults to `username`. Only valid for admin users.
    :param batch_size: Maximum number of folder items to display.
    :param retries: Number of retries if a server request fails.

    .. method:: __len__()

        Number of folder's members.

    .. method:: __getitem__(name)

        Get a domain `name` in the folder.

    .. method:: __delitem__(name)

        Delete a domain `name` in the folder.

    .. method:: __iter__()

        Iterate over folder's members.

        :return: A generator object.

    .. method:: __contains__(name)

        True if `name` is a member of the folder.

    .. method:: __enter__()

        Enter a context manager.

    .. method:: __exit__(*args)

        Exit a context manager.

    .. method:: getACL(username)

        Get ACL for `username`.

    .. method:: getACLs()

        Get all ACLs.

    .. method:: putACL(acl)

        Set `acl` for the folder.

    .. method:: close()

        Close and end folder access.

    .. method:: delete_item(name, keep_root=False)

        Delete a domain `name` in the folder. Optionally delete the folder if
        empty.

    .. attribute:: domain

        UNIX-style (ends with ``/``) folder path if defined or an empty string.

    .. attribute:: parent

        Parent folder path.

    .. attribute:: modified

            Last folder content modification time as a `datetime` object.

    .. attribute:: created

        Folder creation time as a `datetime` object.

    .. attribute:: owner

        Username of the folder's owner.

    .. attribute:: is_folder

        ``True`` if a folder.
