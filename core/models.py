import datetime as dt
import common.constants as constants
from git import Commit


class CommitData(object):
    def __init__(self, commit: Commit):
        self.message_lines = list(
            filter(lambda m: m != '' and not m.startswith(constants.IGNOREֹֹֹ_MESSAGE), commit.message.splitlines()))
        self.message = '\n'.join(self.message_lines)
        self.committed_date = commit.committed_date

    def __str__(self):
        return "message: {}, date: {}".format(self.message.encode('utf-8'),
                                              dt.datetime.fromtimestamp(self.committed_date))


class Commits(object):
    def __init__(self):
        self.commits = []

    def append(self, other: Commit, remove_duplicates=False):
        data_to_append = CommitData(other)
        if remove_duplicates:
            for commit in self.commits:
                common = set(data_to_append.message_lines).intersection(commit.message_lines)
                if len(common) is not 0:
                    print("need to remove duplicates - not implemented")

        self.commits.append(data_to_append)

    def __str__(self):
        st = ''
        for item in self.commits:
            st += str(item) + '\n'

        return st


class RepoStatistics(object):
    def __init__(self):
        self.total_commits = 0
        self.old_commits = 0
        self.external_commits = 0
        self.user_commits = 0
        self.repo_dir = None
        self.repo_name = None
        self.active_branch = None
        self.commit_data = Commits()

    def __str__(self):
        return "Statistics: dir: {}, branch: {}, total: {}, old: {}, external: {}, yours:{}\n commits: \n{}".format(
            self.repo_dir, self.active_branch, self.total_commits, self.old_commits, self.external_commits,
            self.user_commits, self.commit_data)


class GitData(object):
    def __init__(self):
        self.repositories = []

    def append(self, other: RepoStatistics):
        self.repositories.append(other)

    def __str__(self):
        return str(self.repositories)
