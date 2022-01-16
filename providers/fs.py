import os
import datetime as dt
from configparser import NoOptionError

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
        print("Fetching information for: {}({})".format(config.author_name, config.author_email))

        if isinstance(config.root_directory, str):
            config.root_directory = [config.root_directory]

        git_folders = []
        for root in config.root_directory:
            root_folders = self.get_git_folders(root)
            print("Found {} git folders under '{}'.".format(len(root_folders), root))
            git_folders.extend(root_folders)

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
            print('Error at {} message: {}'.format(repo_dir, str(e)))

        return project_info

    def config_reader_get(self, config_reader, key, default=None):
        try:
            return config_reader.get(key)
        except NoOptionError as noe:
            return default

    def get_project_name(self, repo):
        project_name = None
        project_full_name = None
        try:
            for remote in repo.remotes:
                url = self.config_reader_get(remote.config_reader, "url")
                if url.lower().startswith("git@"):
                    # this is github url
                    lower_url = url.lower()
                    project_full_name = url[lower_url.index(":") + 1:lower_url.index(".git")]
                    project_name = project_full_name[project_full_name.index("/") + 1:]
                else:
                    project_name_parts = url.split("/")[3:]
                    project_name = project_name_parts[-1].replace(".git", "")
                    project_full_name = "/".join(project_name_parts).replace(".git", "")
                if project_name is not None and project_full_name is not None:
                    break

        except Exception as e:
            print(str(e))
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
