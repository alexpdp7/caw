import os
import pathlib

import pytest

from caw import archive


caw_test_archive_path = os.environ.get("CAW_TEST_ARCHIVE_PATH")

has_test_archive = pytest.mark.skipif(
    not caw_test_archive_path, reason="no CAW_TEST_ARCHIVE_PATH"
)


@has_test_archive
def test_on_real_archive():
    archive.Archive(pathlib.Path(caw_test_archive_path)).get_tweets()
