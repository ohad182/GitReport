from configuration.config import FileSystemConfig
from core.walker import Walker


def test_report():
    config = FileSystemConfig(
        root_directory="C:\\Git\\", author_name="user name",
        author_email="user@company.com",
        remove_duplicates=True
    )
    walker = Walker(config=config)
    git_data = walker.walk()

    assert git_data is not None
