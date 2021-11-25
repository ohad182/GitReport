from configuration.config import FileSystemConfig, GerritConfig

author_name = "Ohad Cohen"  # the user name on Gerrit/Git
author_email = "ohadc@marvell.com"  # the email associated with the chagnes
ignore_duplicates = True  # weather you want to ignore duplicated commit messages
days_limit = 7  # get past week work log

# root_directory = "C:\\Git\\"  # for fs support - root directory of all your .git projects
root_directory = ["C:\\Git\\", "C:\\Users\\ohadc\\Projects\\", "C:\\Users\\ohadc\\PycharmProjects"]
gerrit_url = "http://vgitil10.il.marvell.com:8080/"  # the url for your gerrit server

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
