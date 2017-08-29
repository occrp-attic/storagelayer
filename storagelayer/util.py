import os
import six
import sys
from hashlib import sha1
from normality import slugify


def checksum(file_name):
    """Generate a hash for a given file name."""
    hash = sha1()
    with open(file_name, 'rb') as fh:
        while True:
            block = fh.read(8192)
            if not block:
                break
            hash.update(block)
    return hash.hexdigest()


def decode_path(file_path):
    """Decode a path specification into unicode."""
    if file_path is None:
        return
    if isinstance(file_path, six.binary_type):
        file_path = file_path.decode(sys.getfilesystemencoding())
    return file_path


def make_filename(file_name, sep='_', default=None, extension=None):
    """Create a secure filename for plain file system storage."""
    if file_name is None:
        return decode_path(default)

    file_name = decode_path(file_name)
    file_name = os.path.basename(file_name)
    file_name, _extension = os.path.splitext(file_name)
    file_name = slugify(file_name, sep=sep) or ''
    file_name = file_name[:250]
    extension = slugify(extension or _extension, sep=sep)
    if extension and len(extension.strip('.')) and len(file_name):
        file_name = '.'.join((file_name, extension))

    if not len(file_name.strip()):
        return decode_path(default)
    return decode_path(file_name)
