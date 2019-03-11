class GitConfig(object):
    def __init__(self, *args, **kwargs):
        self.author_name = kwargs.get("author_name", None)
        self.author_email = kwargs.get("author_email", None)
        self.days_limit = kwargs.get("days_limit", 7)
        self.remove_duplicates = kwargs.get("remove_duplicates", False)


class GerritConfig(GitConfig):
    def __init__(self, *args, **kwargs):
        super(GerritConfig, self).__init__(*args, **kwargs)
        self.url = kwargs.get("url", None)
        self.branch = kwargs.get("branch", None)
        self.project = kwargs.get("project", None)


class FileSystemConfig(GitConfig):
    def __init__(self, *args, **kwargs):
        super(FileSystemConfig, self).__init__(*args, **kwargs)
        self.root_directory = kwargs.get("root_directory", None)
