import os
import pytest
from core.walker import Walker
from core.report import GitReport
from datetime import datetime
from tests.common_config import fs_config


@pytest.fixture(scope="module")
def config():
    config = fs_config
    yield config
    # teardown


def test_report(config):
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
        print("writing report at: {}".format(report_path))
        f.write(report_content)
