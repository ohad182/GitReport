import json
import common.constants as const

from urllib import request
from providers.gerrit.models import *


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
        # suffix = "/changes/?q=owner:\"{}\"&o=MESSAGES".format(email) # gets the messages like jenkins builds info
        # suffix = "/changes/?q=owner:\"{}\"&o=COMMIT_FOOTERS".format(email)
        # suffix = "/changes/?q=owner:\"{}\"&o=DETAILED_ACCOUNTS".format(email) # gets the owner full details
        # suffix = "/changes/?q=owner:\"{}\"&o=ALL_COMMITS".format(email)
        suffix = "/changes/?q=owner:\"{}\"&o=ALL_REVISIONS&o=COMMIT_FOOTERS".format(email)

        # suffix = "/changes/?q=owner:\"{}\"".format(email)
        # COMMIT_FOOTERS
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
