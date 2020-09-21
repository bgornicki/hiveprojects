from time import sleep

from django.conf import settings
from django.utils import timezone

import requests

from profiles.models import Profile, Account, AccountType
from .base_handler import BaseHandler
from package.utils import uniquer

import gitlab


class GitLabHandler(BaseHandler):
    title = "Gitlab"
    url_regex = '(http|https|git)://gitlab.com/'
    url = 'https://gitlab.com'
    repo_regex = r'(?:http|https|git)://gitlab.com/[^/]*/([^/]*)/{0,1}'
    slug_regex = repo_regex


    def __init__(self):
        if settings.GITLAB_TOKEN:
            self.gitlab = gitlab.Gitlab('https://gitlab.com', private_token=settings.GITLAB_TOKEN)
        else:
            self.gitlab = gitlab.Gitlab('https://gitlab.com')

    def _get_repo(self, package):
        try:
            repo_name = package.repo_name()
            print(repo_name)
            if repo_name.endswith("/"):
                repo_name = repo_name[:-1]
            return self.gitlab.projects.get(repo_name.replace('/','%2F'))
        except:
            return None

    def fetch_metadata(self, package):

        repo = self._get_repo(package)
        if repo is None:
            return package

        package.repo_watchers = repo.star_count
        package.repo_forks = repo.forks_count
        package.repo_description = repo.description

        repo_contributors = repo.repository_contributors()

        contributors = []
        gitlab_account_type = AccountType.objects.get(name="GITLAB")

        for contributor in repo_contributors:
            user = self.gitlab.users.list(search=contributor['email'])
            if len(user):
                account_name = Account.syntize_name(account_type='GITLAB', account_name=user[0].username)
                account, created = Account.objects.get_or_create(account_type=gitlab_account_type, name=account_name)
                contributors.append(account)

        package.contributors.set(contributors)
        package.save()

        return package

    def fetch_commits(self, package):
        repo = self._get_repo(package)
        if repo is None:
            return package

        from package.models import Commit  # Added here to avoid circular imports

        commits = repo.commits.list(all=True, query_parameters={'with_stats': 'true'})

        for commit in commits:
            try:
                commit_record, created = Commit.objects.get_or_create(
                    package=package,
                    commit_date=commit.created_at
                )
                if not created:
                    break
            except Commit.MultipleObjectsReturned:
                continue

        package.save()
        return package

repo_handler = GitLabHandler()
