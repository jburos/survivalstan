import os
from fnmatch import fnmatch
import ntpath
import pkg_resources


def _list_files_in_path(path, pattern="*.stan"):
    """
    indexes a directory of stan files
    returns as dictionary containing contents of files
    """

    results = []
    for dirname, subdirs, files in os.walk(path):
        for name in files:
            if fnmatch(name, pattern):
                results.append(os.path.join(dirname, name))
    return(results)


def _read_file(filepath, resource=None):
    """
    reads file contents from disk

    Parameters
    ----------
    filepath (string):
        path to file (can be relative or absolute)
    resource (string, optional):
        if given, path is relative to package install root
        used to load stan files provided by packages
        (e.g. those within a package library)

    Returns
    -------
    The specifics of the return type depend on the value of `resource`.
        - if resource is None, returns contents of file as a character string
        - otherwise, returns a "resource_string" which
            acts as a character string but technically isn't one.
    """
    print(filepath)
    if not(resource):
        with open(filepath, 'r') as myfile:
            data = myfile.read()
    else:
        data = pkg_resources.resource_string(
            resource, filepath)
    return data


def read_files(path, pattern='*.stan', encoding="utf-8", resource=None):
    """
    Reads file contents from a directory path into memory. Returns a 
    dictionary of file names: file contents.

    Is intended to be used to load a directory of stan files into an object.

    Parameters
    ----------
    path (string):
        directory path (can be relative or absolute)
    pattern (string, optional):
        regex pattern applied to files on import
        defaults to "*.stan"
    encoding (string, optional):
        encoding to use when importing files
        defaults to "UTF-8"
    resource (string, optional):
        if given, path is relative to package install root
        used to load stan files provided by packages
        (e.g. those within a package library)

    Returns
    -------
    The specifics of the return type depend on the value of `resource`.
        - if resource is None, returns contents of file as a character string
        - otherwise, returns a "resource_string" which
            acts as a character string but technically isn't one.
    """
    files = _list_files_in_path(path=path, pattern=pattern)
    results = {}
    for file in files:
        file_data = {}
        file_data['path'] = file
        file_data['basename'] = ntpath.basename(file)
        file_data['code'] = _read_file(
            file,
            resource=resource).decode(encoding)
        results[file_data['basename']] = file_data['code']
    return(results)
