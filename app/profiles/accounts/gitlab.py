from time import sleep

from django.conf import settings
from django.utils import timezone

import gitlab
from .base_handler import BaseHandler


class GitLabHandler(BaseHandler):

    def __init__(self):
        if settings.GITLAB_TOKEN:
            self.gitlab = gitlab.Gitlab('https://gitlab.com', private_token=settings.GITLAB_TOKEN)
        else:
            self.gitlab = gitlab.Gitlab('https://gitlab.com/')

    def get_account(self, name):
        account = self.gitlab.users.list(username=name)[0]
        return account


account_handler = GitLabHandler()
