from configuration.config import GerritConfig
from core.walker import Walker


def test_gerrit_changes():
    config = GerritConfig(
        root_directory="C:\\Git\\", author_name="user name",
        author_email="user@company.com",
        remove_duplicates=True,
        url="http://gerrit.com"
    )
    walker = Walker(config=config)
    git_data = walker.walk()
