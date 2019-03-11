import os
from configuration.config import FileSystemConfig
from core.walker import Walker
from core.report import GitReport
from datetime import datetime


def get_week_year():
    week = datetime.today().isocalendar()[1]
    year = datetime.today().year
    return "{}-{}".format(week, year)


def name_extraction(repo, parent=None):
    if repo.repo_name is not None:
        return repo.repo_name.rstrip("\'")
    repo_name = os.path.basename(os.path.dirname(repo.repo_dir) if parent is None else parent)
    return name_extraction(repo, os.path.dirname(
        repo.repo_dir if parent is None else parent)) if repo_name == repo.active_branch.name else repo_name


def test_report():
    config = FileSystemConfig(
        root_directory="C:\\Git\\", author_name="user name",
        author_email="user@company.com",
        remove_duplicates=True
    )
    walker = Walker(config=config)
    git_data = walker.walk()

    reporter = GitReport(git_data=git_data,
                         project_name_extractor=name_extraction
                         )

    report_content = reporter.generate()
    assert git_data is not None

    report_name = '../assets/weekly_report{}.html'.format(get_week_year())
    assert report_content is not None

    report_path = os.path.realpath(os.path.join(os.path.dirname(__file__), report_name))

    report_dir = os.path.dirname(os.path.abspath(report_path))

    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    with open(report_path, 'w+') as f:
        f.write(report_content)
