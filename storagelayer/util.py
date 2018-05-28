import six
import sys
import binascii

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


BUF_SIZE = 1024 * 1024 * 16
CRYPTO = default_backend()


def checksum(file_name):
    """Generate a hash for a given file name."""
    digest = hashes.Hash(hashes.SHA1(), backend=CRYPTO)
    with open(file_name, 'rb') as fh:
        while True:
            block = fh.read(BUF_SIZE)
            if not block:
                break
            digest.update(block)
    hexdigest = binascii.hexlify(digest.finalize())
    return hexdigest.decode('utf-8')


def decode_path(file_path):
    """Decode a path specification into unicode."""
    if file_path is None:
        return
    if isinstance(file_path, six.binary_type):
        file_path = file_path.decode(sys.getfilesystemencoding())
    return file_path
