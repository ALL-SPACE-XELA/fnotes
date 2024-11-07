
import pytest
from fnote.file import NFile
import shutil

DO_CLEANUP = True
ROOT_DIR = "test_data_dir"

@pytest.fixture(autouse=True)
def run_around_tests():
    assert True
    yield
    # teardown
    if DO_CLEANUP:
        print("Removing {} and all its contents".format(ROOT_DIR))
        shutil.rmtree(ROOT_DIR)
    assert True

def test_get_root_dir():
    # this is just a test to check we can change root dir
    nfile = NFile("tmpfile", ROOT_DIR)
    assert  nfile.get_root_dir() == ROOT_DIR

