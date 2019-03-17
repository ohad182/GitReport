import datetime as dt
from core.models import UserInfo, ProjectInfo, CommitInfo
from providers.base import BaseGitProvider
from configuration.config import GerritConfig
from providers.gerrit.client import Gerrit


class GerritProvider(BaseGitProvider):
    def __init__(self, *args, **kwargs):
        super(GerritProvider, self).__init__(*args, **kwargs)
        self.gerrit_client = Gerrit(gerrit_url=self.config.url) if self.config is not None else None

    def walk(self, config: GerritConfig) -> UserInfo:
        user_info = UserInfo()

        if config is not None:
            self.config = config
            self.gerrit_client = Gerrit(gerrit_url=self.config.url)

        user_changes = self.gerrit_client.changes(config.author_email)

        """ changes from gerrit are sorted by date [0]-latest [n]-oldest"""
        min_date = dt.datetime.now() - dt.timedelta(days=config.days_limit)

        self.organize_changes(user_changes, user_info, min_date)

        return user_info

    def organize_changes(self, user_changes, user_info: UserInfo, min_date):
        if user_info is None:
            user_info = UserInfo()

        for change in user_changes:

            current_project = user_info.get_project(change.project_name)
            if current_project is None:
                """ this change project is not in the model"""
                current_project = ProjectInfo(full_name=change.project_full_name, name=change.project_name, location="",
                                              branch=change.branch)
                user_info.projects.append(current_project)

            current_project.total_commits += 1
            if min_date < change.created:
                commit = CommitInfo(commit_date=change.created, commit_message=change.commit_message)

                current_project.append_commit(commit, self.config.remove_duplicates)
                current_project.my_commits += 1
            else:
                current_project.old_commits += 1
