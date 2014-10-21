
""" Utility functions. """

import collections
import os
import unicodedata
import re
import shutil


# Named tuples for file and directory information.
DirInfo = collections.namedtuple('DirInfo', 'name, path')
FileInfo = collections.namedtuple('FileInfo', 'name, path, base, ext')


def subdirs(directory):
    """ Returns a list of subdirectories of the specified directory. """
    directories = []
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isdir(path):
            directories.append(DirInfo(name, path))
    return directories


def files(directory):
    """ Returns a list of files in the specified directory. """
    files = []
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isfile(path):
            base, ext = os.path.splitext(name)
            files.append(FileInfo(name, path, base, ext))
    return files


def textfiles(directory):
    """ Returns a list of text files in the specified directory. """
    extensions = ('.txt', '.stx', '.md', '.markdown')
    return [fi for fi in files(directory) if fi.ext in extensions]


def slugify(s):
    """ Slug preparation function. Used to sanitize url components, etc. """
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore').decode('ascii')
    s = s.lower()
    s = re.sub(r'[^a-z0-9-]+', '-', s)
    s = re.sub(r'--+', '-', s)
    return s.strip('-')


def titlecase(s):
    """ Returns a titlecased version of the supplied string. """
    return re.sub(
        r"[A-Za-z]+('[A-Za-z]+)?",
        lambda m: m.group(0)[0].upper() + m.group(0)[1:],
        s
    )


def copydir(srcdir, dstdir, skip=True):
    """ Copies `srcdir` to `dstdir`, creating `dstdir` if necessary. """

    if not os.path.exists(dstdir):
        os.makedirs(dstdir)

    for name in os.listdir(srcdir):
        src = os.path.join(srcdir, name)
        dst = os.path.join(dstdir, name)

        if skip and name.startswith('@'):
            continue

        if os.path.isfile(src):
            shutil.copy2(src, dst)

        elif os.path.isdir(src):
            copy_contents(src, dst, False)


def clear_directory(dirpath):
    """ Clears the contents of a directory. """
    if os.path.isdir(dirpath):
        for name in os.listdir(dirpath):
            path = os.path.join(dirpath, name)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)


def writefile(filepath, content):
    """ Writes a string to a file. """
    if not os.path.isdir(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)


def make_redirect(filepath, url):
    """ Creates a redirect page at the specified filepath. """
    html = """\
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Redirect</title>
        <meta http-equiv="refresh" content="0; url=%s">
    </head>
    <body></body>
</html>
""" % url
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(html)
