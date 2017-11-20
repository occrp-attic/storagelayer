import six
import sys
from hashlib import sha1


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
