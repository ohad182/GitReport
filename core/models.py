import datetime as dt
import common.constants as constants
from git import Commit


class CommitInfo(object):
    """
    A model class to describe commit info (relevant to the report)
    """

    def __init__(self, **kwargs):
        msg = kwargs.get("commit_message", "")
        self.message_lines = list(
            filter(lambda m: m != '' and not m.startswith(constants.IGNORE_MESSAGE), msg.splitlines()))
        self.message = '\n'.join(self.message_lines)
        self.commit_date = kwargs.get("commit_date", None)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.message == other.message and \
                   self.commit_date == other.commit_date and \
                   self.message_lines == other.message_lines
        else:
            return False


class ProjectInfo(object):
    def __init__(self, **kwargs):
        self.full_name = kwargs.get("full_name", None)
        self.name = kwargs.get("name", None)
        self.total_commits = kwargs.get("total_commits", 0)
        self.old_commits = kwargs.get("old_commits", 0)
        self.other_commits = kwargs.get("other_commits", 0)
        self.my_commits = kwargs.get("my_commits", 0)
        self.location = kwargs.get("location", None)
        self.branch = kwargs.get("branch", None)
        self.commits = kwargs.get("commits", [])

    def __str__(self):
        return "{} - {}".format(self.name, self.branch)

    def append_commit(self, commit: CommitInfo, ignore_duplicates=False):
        duplicate = False
        if ignore_duplicates:
            existing = next((x for x in self.commits if x == commit), None)
            duplicate = existing is not None
        if not duplicate:
            self.commits.append(commit)


class UserInfo(object):
    def __init__(self):
        self.projects = []

    def get_project(self, name):
        return next((x for x in self.projects if x.name == name), None)
