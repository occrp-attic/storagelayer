import logging

from storagelayer.file import FileArchive
from storagelayer.s3 import S3Archive
from storagelayer.util import checksum  # noqa

logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)

ARCHIVE_FILE = 'file'
ARCHIVE_S3 = 's3'


def init(archive_type, path=None, bucket=None, aws_key_id=None,
         aws_secret=None, aws_region=None):
    """Instantiate an archive object.

    Arguments to this should probably be wrapped in a nicer way in the future.
    """
    archive_type = archive_type or ARCHIVE_FILE
    archive_type = archive_type.lower().strip()

    if archive_type == ARCHIVE_S3:
        return S3Archive(bucket=bucket, aws_key_id=aws_key_id,
                         aws_secret=aws_secret, aws_region=aws_region)

    return FileArchive(path=path)
