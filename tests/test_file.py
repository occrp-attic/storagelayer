import os
import shutil
import tempfile
from unittest import TestCase

import storagelayer


class FileArchiveTest(TestCase):

    def setUp(self):
        self.path = os.path.join(tempfile.gettempdir(), 'storagelayer_test')
        self.archive = storagelayer.init('file', path=self.path)
        self.file = os.path.abspath(__file__)

    def tearDown(self):
        if os.path.exists(self.path):
            shutil.rmtree(self.path)

    def test_basic_archive(self):
        checksum = storagelayer.checksum(self.file)
        assert checksum is not None, checksum
        out = self.archive.archive_file(self.file)
        assert checksum == out, (checksum, out)
        out2 = self.archive.archive_file(self.file)
        assert out == out2, (out, out2)

    def test_basic_archive_with_checksum(self):
        checksum = 'banana'
        out = self.archive.archive_file(self.file, checksum)
        assert checksum == out, (checksum, out)

    def test_generate_url(self):
        out = self.archive.archive_file(self.file)
        url = self.archive.generate_url(out)
        assert url is None, url

    def test_load_file(self):
        out = self.archive.archive_file(self.file)
        path = self.archive.load_file(out)
        assert path is not None, path
        assert path.startswith(self.path)
        assert os.path.isfile(path), path

    def test_cleanup_file(self):
        out = self.archive.archive_file(self.file)
        self.archive.cleanup_file(out)
        path = self.archive.load_file(out)
        assert os.path.isfile(path), path
