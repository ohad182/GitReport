import os
import pytest
from tests.common_config import gerrit_config
from configuration.config import GerritConfig
from core.walker import Walker
from providers.gerrit import Gerrit


@pytest.fixture(scope="module")
def config():
    config = gerrit_config
    yield config
    # teardown


def test_gerrit_changes(config):
    gerrit = Gerrit()
    assert gerrit.changes(config.author_email) is not None


def test_gerrit_walker(config):
    walker = Walker(config=config)
    user_info = walker.walk()

    assert user_info is not None
