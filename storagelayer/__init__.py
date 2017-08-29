from storagelayer.file import FileArchive
from storagelayer.s3 import S3Archive
from storagelayer.util import checksum  # noqa


def archive_from_config(config):
    """Instantiate an archive object."""
    archive_type = config.get('ARCHIVE_TYPE', 'file').lower()
    if archive_type == 's3':
        return S3Archive(config)
    return FileArchive(config)
