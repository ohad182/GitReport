import os
import datetime as dt
import common.constants as constants
from git import Repo

from core.models import RepoStatistics, GitData
from providers.base import BaseGitProvider
from configuration.config import FileSystemConfig


class FileSystemProvider(BaseGitProvider):
    def __init__(self, *args, **kwargs):
        super(FileSystemProvider, self).__init__(*args, **kwargs)
        self.default_git_name = constants.GIT_EXT
        self.ignore_folders = constants.IGNORE_FOLDERS

    def walk(self, config: FileSystemConfig) -> GitData:
        git_folders = self.get_git_folders(config.root_directory)
        print("Found {} git folders.".format(len(git_folders)))

        git_data = GitData()
        for folder in sorted(git_folders):
            # print(folder)
            repo_data = self.get_repo_data(folder, config.author_name, config.author_email, config.days_limit,
                                           config.remove_duplicates)
            if repo_data.user_commits > 0:
                git_data.append(repo_data)
                # print(repo_data)

        return git_data

    def get_repo_data(self, repo_dir, name, email, days, remove_duplicates):
        data = RepoStatistics()
        data.repo_dir = repo_dir
        try:
            repo = Repo(repo_dir)

            data.active_branch = repo.active_branch
            data.repo_name = self.get_project_name(repo)
            if repo.bare:
                """
                this is not .git folder
                """
                print("this is not a git repo: {}".format(repo_dir))
            else:
                min_date = dt.datetime.now() - dt.timedelta(days=days)
                for commit in repo.iter_commits():
                    if commit.author.name == name or commit.author.email == email:
                        if min_date < dt.datetime.fromtimestamp(commit.committed_date):
                            data.commit_data.append(commit, remove_duplicates)
                            data.user_commits = data.user_commits + 1
                        else:
                            data.old_commits = data.old_commits + 1
                    else:
                        data.external_commits = data.external_commits + 1
        except Exception as e:
            print('Error at {} message: {}'.format(repo_dir, e.message))
        return data

    def get_project_name(self, repo):
        project_name = None
        try:
            url = str(repo.remote("origin").config_reader.config._sections[u'remote "origin"'][u'url'])
            project_name = str(url.encode('utf-8')).rsplit('/', 1)[-1]
        except Exception as e:
            print(e.message)
        return project_name

    def get_git_folders(self, root):

        dir_name = os.path.split(root)[-1] if os.path.isdir(root) else os.path.split(os.path.dirname(root))[-1]

        if dir_name == self.default_git_name:
            return [root]
        else:
            git_dirs = []
            for name in os.listdir(root):
                if os.path.isdir(os.path.join(root, name)):
                    if name == self.default_git_name:
                        git_dirs.append(os.path.join(root, name))
                    elif not name.startswith('.') and name not in self.ignore_folders:
                        additional_gits = self.get_git_folders(os.path.join(root, name))
                        if additional_gits:
                            git_dirs.extend(additional_gits)
            return git_dirs
