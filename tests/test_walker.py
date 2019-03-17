import os
from configuration.config import FileSystemConfig
from core.walker import Walker
from core.report import GitReport
from datetime import datetime


def test_report():
    config = FileSystemConfig(
        root_directory="C:\\Git\\", author_name="user name",
        author_email="user@company.com",
        remove_duplicates=True
    )
    walker = Walker(config=config)
    git_data = walker.walk()

    reporter = GitReport(git_data=git_data)

    report_content = reporter.generate()
    assert git_data is not None

    report_name = '../assets/weekly_report{}.html'.format("-".join(str(x) for x in datetime.today().isocalendar()[:2]))
    assert report_content is not None

    report_path = os.path.realpath(os.path.join(os.path.dirname(__file__), report_name))

    report_dir = os.path.dirname(os.path.abspath(report_path))

    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    with open(report_path, 'w+') as f:
        f.write(report_content)
