import os
import datetime as dt
import common.constants as constants
from git import Repo

from core.models import UserInfo, ProjectInfo, CommitInfo
from providers.base import BaseGitProvider
from configuration.config import FileSystemConfig


class FileSystemProvider(BaseGitProvider):
    def __init__(self, *args, **kwargs):
        super(FileSystemProvider, self).__init__(*args, **kwargs)
        self.default_git_name = constants.GIT_EXT
        self.ignore_folders = constants.IGNORE_FOLDERS

    def walk(self, config: FileSystemConfig) -> UserInfo:
        git_folders = self.get_git_folders(config.root_directory)
        print("Found {} git folders.".format(len(git_folders)))

        user_info = UserInfo()
        for folder in sorted(git_folders):
            project_info = self.get_repo_data(folder, config.author_name, config.author_email, config.days_limit,
                                              config.remove_duplicates)
            if project_info.my_commits > 0:
                user_info.projects.append(project_info)

        return user_info

    def get_repo_data(self, repo_dir, name, email, days, remove_duplicates) -> ProjectInfo:
        project_info = ProjectInfo(location=repo_dir)
        try:
            repo = Repo(repo_dir)

            project_info.branch = repo.active_branch
            project_info.name, project_info.full_name = self.get_project_name(repo)
            if repo.bare:
                """
                this is not .git folder
                """
                print("this is not a git repo: {}".format(repo_dir))
            else:
                min_date = dt.datetime.now() - dt.timedelta(days=days)
                for commit in repo.iter_commits():
                    if commit.author.name == name or commit.author.email == email:
                        commit_date = dt.datetime.fromtimestamp(commit.committed_date)
                        if min_date < commit_date:
                            project_info.append_commit(
                                CommitInfo(commit_date=commit_date, commit_message=commit.message),
                                remove_duplicates)
                            project_info.my_commits += 1
                        else:
                            project_info.old_commits += 1
                    else:
                        project_info.other_commits += 1
        except Exception as e:
            print('Error at {} message: {}'.format(repo_dir, e.message))

        return project_info

    def get_project_name(self, repo):
        project_name = None
        project_full_name = None
        try:
            url = repo.remote("origin").config_reader.config._sections[u'remote "origin"'][u'url']
            project_name_parts = url.split("/")[3:]
            project_name = project_name_parts[-1]
            project_full_name = "/".join(project_name_parts)

        except Exception as e:
            print(e.message)
        return project_name, project_full_name

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
