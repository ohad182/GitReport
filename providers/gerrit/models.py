import datetime

"""
Model object based on https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html
"""


def gerrit_time(time_str) -> datetime:
    if time_str is not None:
        return datetime.datetime.strptime(time_str[:time_str.index(".")], "%Y-%m-%d %H:%M:%S")
    else:
        return None


class ChangeInfo(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.project_full_name = kwargs.get("project", None)
        self.project_name = self.project_full_name[self.project_full_name.rfind("/") + 1:]
        self.branch = kwargs.get("branch", None)
        self.hashtags = kwargs.get("hashtags", None)
        self.topic = kwargs.get("topic", None)
        self.change_id = kwargs.get("change_id", None)
        self.subject = kwargs.get("subject", None)
        self.status = kwargs.get("status", None)
        self.created = gerrit_time(kwargs.get("created", None))
        self.updated = gerrit_time(kwargs.get("updated", None))
        self.submitted = gerrit_time(kwargs.get("submitted", None))
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
        self._more_changes = kwargs.get("_more_changes", None)
        self.problems = kwargs.get("problems", None)
        self.submittable = kwargs.get("submittable", None)
        self.current_revision = kwargs.get("current_revision", None)
        revisions_dict = kwargs.get("revisions", None)
        self.commit_message = None
        if revisions_dict is not None:
            self.revisions = []
            for revision_id, revision in revisions_dict.items():
                revision_model = RevisionInfo(**revision)
                self.revisions.append(revision_model)
                if revision_model.message:
                    if self.commit_message is None:
                        self.commit_message = ""
                    self.commit_message += revision_model.message


class AccountInfo(object):
    def __init__(self, **kwargs):
        self._account_id = kwargs.get("_account_id", None)
        self.name = kwargs.get("name", None)
        self.email = kwargs.get("email", None)
        self.secondary_emails = kwargs.get("secondary_emails", None)
        self.username = kwargs.get("username", None)
        self._more_accounts = kwargs.get("_more_accounts", None)


class RevisionInfo(object):
    def __init__(self, **kwargs):
        self.kind = kwargs.get("kind", None)
        self._number = kwargs.get("_number", None)
        self.created = kwargs.get("created", None)
        self.uploader = kwargs.get("uploader", None)
        self.ref = kwargs.get("ref", None)
        self.fetch = kwargs.get("fetch", None)
        self.commit = kwargs.get("commit", None)
        self.files = kwargs.get("files", None)
        self.actions = kwargs.get("actions", None)
        self.reviewed = kwargs.get("reviewed", None)
        self.message = kwargs.get("messageWithFooter", kwargs.get("commit_with_footers", None))
        self.push_certificate = kwargs.get("push_certificate", None)
        self.description = kwargs.get("description", None)
