from configuration.config import FileSystemConfig, GerritConfig

author_name = "User Name"  # the user name on Gerrit/Git
author_email = "user@company.com"  # the email associated with the chagnes
ignore_duplicates = True  # weather you want to ignore duplicated commit messages
days_limit = 7  # get past week work log

root_directory = "C:\\Git\\"  # for fs support - root directory of all your .git projects
gerrit_url = "http://gerrit.com"  # the url for your gerrit server

fs_config = FileSystemConfig(
    root_directory=root_directory,
    author_name=author_name,
    author_email=author_email,
    remove_duplicates=ignore_duplicates,
    days_limit=days_limit
)

gerrit_config = GerritConfig(
    url=gerrit_url,
    author_name=author_name,
    author_email=author_email,
    remove_duplicates=ignore_duplicates,
    days_limit=days_limit
)
