import os
from pathlib import Path

import pytest


@pytest.fixture()
def with_tmp_path(tmp_path):
    orig_dir = Path.cwd()
    try:
        os.chdir(tmp_path)
        yield tmp_path
    except:  # noqa
        os.chdir(orig_dir)
