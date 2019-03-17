from configuration.config import GerritConfig
from core.walker import Walker


def test_gerrit_changes():
    from providers.gerrit import Gerrit
    config = GerritConfig(
        root_directory="C:\\Git\\", author_name="user name",
        author_email="user@company.com",
        remove_duplicates=True,
        url="http://gerrit.com",
        days_limit=7
    )
    gerrit = Gerrit()

    assert gerrit.changes(config.author_email) is not None


def test_gerrit_walker():
    config = GerritConfig(
        root_directory="C:\\Git\\", author_name="Ohad Cohen",
        author_email="ohadc@marvell.com",
        remove_duplicates=True,
        url="http://vgitil10.il.marvell.com:8080",
        days_limit=7
    )
    walker = Walker(config=config)
    git_data = walker.walk()
