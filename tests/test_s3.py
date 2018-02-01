import os
from unittest import TestCase

from moto import mock_s3

import storagelayer


class FileArchiveTest(TestCase):

    def setUp(self):
        self.mock = mock_s3()
        self.mock.start()
        self.archive = storagelayer.init('s3', bucket='foo')
        self.file = os.path.abspath(__file__)

    def tearDown(self):
        self.mock.stop()

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
        # assert False, url
        assert url is not None, url

    def test_load_file(self):
        out = self.archive.archive_file(self.file)
        path = self.archive.load_file(out)
        assert path is not None, path
        assert os.path.isfile(path), path

    def test_cleanup_file(self):
        out = self.archive.archive_file(self.file)
        self.archive.cleanup_file(out)
        path = self.archive.load_file(out)
        assert os.path.isfile(path), path
        self.archive.cleanup_file(out)
        assert not os.path.isfile(path), path
