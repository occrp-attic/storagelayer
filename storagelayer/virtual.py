import os
import shutil
import logging
import tempfile
import threading
from normality import safe_filename

from storagelayer.archive import Archive

log = logging.getLogger(__name__)


class VirtualArchive(Archive):

    def __init__(self):
        self.local = threading.local()

    def _get_local_prefix(self, content_hash, temp_path=None):
        """Determine a temporary path for the file on the local file
        system."""
        if temp_path is None:
            if not hasattr(self.local, 'dir'):
                self.local.dir = tempfile.mkdtemp(prefix=self.bucket)
            temp_path = self.local.dir
        path_name = '%s.slayer' % content_hash
        return os.path.join(temp_path, path_name)

    def _local_path(self, content_hash, file_name, temp_path):
        path = self._get_local_prefix(content_hash, temp_path=temp_path)
        try:
            os.makedirs(path)
        except Exception:
            pass
        file_name = safe_filename(file_name, default='data')
        return os.path.join(path, file_name)

    def cleanup_file(self, content_hash, temp_path=None):
        """Delete the local cached version of the file."""
        if content_hash is None:
            return
        path = self._get_local_prefix(content_hash, temp_path=temp_path)
        if os.path.isdir(path):
            shutil.rmtree(path)
