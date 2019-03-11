from abc import ABC, abstractmethod
from configuration.config import GitConfig


class BaseGitProvider(ABC):  # ABCMeta
    def __init__(self, *args, **kwargs):
        self.config = kwargs.get("config", None)

    @abstractmethod
    def walk(self, config: GitConfig):
        pass
