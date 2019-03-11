import common.constants as constants
from configuration.config import *
from providers.fs import FileSystemProvider
from providers.gerrit import GerritProvider


class Walker(object):
    def __init__(self, **kwargs):
        self.config = kwargs.get("config", None)
        self.providers = {
            constants.LOCAL: FileSystemProvider(),
            constants.GERRIT: GerritProvider()
        }

    def walk(self, i_config=None):
        if i_config:
            self.config = i_config
        if self.config:
            if isinstance(self.config, FileSystemConfig):
                return self.providers[constants.LOCAL].walk(self.config)
            elif isinstance(self.config, GerritConfig):
                return self.providers[constants.GERRIT].walk(self.config)
            else:
                raise Exception("Unknown Configuration Type")
