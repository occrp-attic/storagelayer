import os
import shutil
import logging
import threading
import tempfile
from normality import safe_filename
import boto3
# from botocore.client import Config
from botocore.exceptions import ClientError

from storagelayer.archive import Archive
from storagelayer.util import checksum

log = logging.getLogger(__name__)


class S3Archive(Archive):
    TIMEOUT = 84600
    DEFAULT_REGION = 'eu-west-1'

    def __init__(self, bucket=None, aws_key_id=None, aws_secret=None,
                 aws_region=None):
        region_name = aws_region or self.DEFAULT_REGION
        self.client = boto3.client('s3',
                                   region_name=region_name,
                                   aws_access_key_id=aws_key_id,
                                   aws_secret_access_key=aws_secret)
        # config=Config(signature_version='s3v4'))
        self.bucket = bucket
        self.local = threading.local()
        log.info("Archive: s3://%s", bucket)

        try:
            self.client.head_bucket(Bucket=bucket)
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                self.client.create_bucket(Bucket=bucket)
            else:
                log.exception("Could not check bucket")

        # Make sure bucket policy is set correctly.
        config = {
            'CORSRules': [
                {
                    'AllowedMethods': ['GET'],
                    'AllowedOrigins': ['*'],
                    'AllowedHeaders': ['*'],
                    'ExposeHeaders': ['Accept-Ranges', 'Content-Encoding',
                                      'Content-Length', 'Content-Range'],
                    'MaxAgeSeconds': self.TIMEOUT
                }
            ]
        }
        try:
            self.client.put_bucket_cors(Bucket=bucket,
                                        CORSConfiguration=config)
        except ClientError as e:
            log.warning("Could not update CORS")

    def _locate_key(self, content_hash):
        """Check if a file with the given hash exists on S3."""
        if content_hash is None:
            return
        prefix = self._get_prefix(content_hash)
        if prefix is None:
            return
        res = self.client.list_objects(MaxKeys=1,
                                       Bucket=self.bucket,
                                       Prefix=prefix)
        for obj in res.get('Contents', []):
            return obj.get('Key')

    def archive_file(self, file_path, content_hash=None):
        """Store the file located at the given path on S3, based on a path
        made up from its SHA1 content hash."""
        if content_hash is None:
            content_hash = checksum(file_path)

        obj = self._locate_key(content_hash)
        if obj is None:
            path = os.path.join(self._get_prefix(content_hash), 'data')
            self.client.upload_file(file_path, self.bucket, path)
        return content_hash

    def _get_local_prefix(self, content_hash, temp_path=None):
        """Determine a temporary path for the file on the local file
        system."""
        if temp_path is None:
            if not hasattr(self.local, 'dir'):
                self.local.dir = tempfile.mkdtemp(prefix=self.bucket)
            temp_path = self.local.dir
        path_name = '%s.slayer' % content_hash
        return os.path.join(temp_path, path_name)

    def load_file(self, content_hash, file_name=None, temp_path=None):
        """Retrieve a file from S3 storage and put it onto the local file
        system for further processing."""
        key = self._locate_key(content_hash)
        if key is not None:
            path = self._get_local_prefix(content_hash, temp_path=temp_path)
            try:
                os.makedirs(path)
            except Exception:
                pass
            file_name = safe_filename(file_name, default='data')
            path = os.path.join(path, file_name)
            self.client.download_file(self.bucket, key, path)
            return path

    def cleanup_file(self, content_hash, temp_path=None):
        """Delete the local cached version of the file."""
        if content_hash is None:
            return
        path = self._get_local_prefix(content_hash, temp_path=temp_path)
        if os.path.isdir(path):
            shutil.rmtree(path)

    def generate_url(self, content_hash, file_name=None, mime_type=None):
        key = self._locate_key(content_hash)
        if key is None:
            return
        params = {
            'Bucket': self.bucket,
            'Key': key
        }
        if mime_type:
            params['ResponseContentType'] = mime_type
        if file_name:
            disposition = 'inline; filename=%s' % file_name
            params['ResponseContentDisposition'] = disposition
        return self.client.generate_presigned_url('get_object',
                                                  Params=params,
                                                  ExpiresIn=self.TIMEOUT)
