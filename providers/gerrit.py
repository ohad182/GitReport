import json
import common.constants as const
from core.models import GitData
from providers.base import BaseGitProvider
from configuration.config import GerritConfig
from urllib import request


class GerritProvider(BaseGitProvider):
    def __init__(self, *args, **kwargs):
        super(GerritProvider, self).__init__(*args, **kwargs)
        self.gerrit_client = Gerrit(gerrit_url=self.config.url) if self.config is not None else None

    def walk(self, config: GerritConfig) -> GitData:
        git_data = GitData()

        if config is not None:
            self.config = config
            self.gerrit_client = Gerrit(gerrit_url=self.config.url)

        user_changes = self.gerrit_client.changes(config.author_email)
        # TODO: process these changes

        return git_data


class Gerrit(object):
    """
        Gerrit REST client basic implementation (for app needs)
    """

    def __init__(self, **kwargs):
        self.url = kwargs.get("gerrit_url", const.GERRIT)
        self.magic_prefix = kwargs.get("magic_prefix", const.GERRIT_MAGIC_PREFIX)

    def query(self):
        raise NotImplementedError("Gerrit.query is not implemented yet")

    def changes(self, email):
        """
        performs a gerrit changes query for the configured owner email
        :param email: the owner email
        :return: a list of ChangeInfo objects that describes the changes this owner has
        """
        suffix = "/changes/?q=owner:\"{}\"".format(email)
        data = self._get(url="{}{}".format(self.url, suffix))
        result = []
        if data is not None:
            for item in data:
                result.append(ChangeInfo(**item))

        return result

    def _get(self, **kwargs):
        headers = kwargs.get("headers", {'Content-Type': 'application/json'})
        url = kwargs.get("url")
        req = request.Request(url=url, headers=headers)
        resp = request.urlopen(req)
        resp_data = resp.read()
        encoding = resp.info().get_content_charset('utf-8')
        decoded_resp_data = resp_data.decode(encoding)
        gerrit_escaped = decoded_resp_data.replace(self.magic_prefix, "", 1)
        obj = json.loads(gerrit_escaped)
        return obj


class ChangeInfo(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.project = kwargs.get("project", None)
        self.branch = kwargs.get("branch", None)
        self.hashtags = kwargs.get("hashtags", None)
        self.topic = kwargs.get("topic", None)
        self.change_id = kwargs.get("change_id", None)
        self.subject = kwargs.get("subject", None)
        self.status = kwargs.get("status", None)
        self.created = kwargs.get("created", None)
        self.updated = kwargs.get("updated", None)
        self.submitted = kwargs.get("submitted", None)
        self.starred = kwargs.get("starred", None)
        self.stars = kwargs.get("stars", None)
        self.reviewed = kwargs.get("reviewed", None)
        self.submit_type = kwargs.get("submit_type", None)
        self.mergeable = kwargs.get("mergeable", None)
        self.insertions = kwargs.get("insertions", None)
        self.deletions = kwargs.get("deletions", None)
        self._number = kwargs.get("_number", None)
        self.owner = AccountInfo(**kwargs.get("owner", {}))
        self.actions = kwargs.get("actions", None)
        self.labels = kwargs.get("labels", None)
        self.permitted_labels = kwargs.get("permitted_labels", None)
        self.removeable_reviewers = kwargs.get("removeable_reviewers", None)
        self.reviewers = kwargs.get("reviewers", None)
        self.reviewer_updates = kwargs.get("reviewer_updates", None)
        self.messages = kwargs.get("messages", None)
        self.current_revision = kwargs.get("current_revision", None)
        self.revisions = kwargs.get("revisions", None)
        self._more_changes = kwargs.get("_more_changes", None)
        self.problems = kwargs.get("problems", None)
        self.submittable = kwargs.get("submittable", None)


class AccountInfo(object):
    def __init__(self, **kwargs):
        self._account_id = kwargs.get("_account_id", None)
        self.name = kwargs.get("name", None)
        self.email = kwargs.get("email", None)
        self.secondary_emails = kwargs.get("secondary_emails", None)
        self.username = kwargs.get("username", None)
        self._more_accounts = kwargs.get("_more_accounts", None)
