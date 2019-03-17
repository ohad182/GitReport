import pytest
from tests.common_config import fs_config
from core.walker import Walker


@pytest.fixture(scope="module")
def config():
    config = fs_config
    yield config
    # teardown


def test_report(config):
    walker = Walker(config=config)
    git_data = walker.walk()

    assert git_data is not None
