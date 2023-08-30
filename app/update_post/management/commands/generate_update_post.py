from django.template.loader import get_template
from django.urls import reverse

from package.templatetags.package_tags import thumb
from settings.base import SITE_URL
import datetime

try:
    from django.core.management.base import NoArgsCommand
except ImportError:
    from django.core.management import BaseCommand as NoArgsCommand
from package.models import Project
from update_post.models import UpdatePost

from django.conf import settings

import random
import string

from beem import Hive

class Command(NoArgsCommand):

    def handle(self, *args, **options):

        last_post = UpdatePost.objects.latest()

        if last_post is not None:
            projects = Project.objects.published().filter(publication_time__gt=last_post.publish_date).order_by('-publication_time')
        else:
            projects = Project.objects.published().order_by('-publication_time')

        if len(projects) >= 1:
            items = []
            for project in projects:
                project_url = "{}{}".format(SITE_URL, reverse("package", kwargs={"slug": project.slug}))
                hive_team_members = ", ".join([
                    user.display_name
                    for user in  project.team_members.hive_users()
                ])
                category_url = "{}{}".format(SITE_URL, reverse("category", kwargs={"slug": project.category.slug}))
                project_image_url = "{}{}".format(SITE_URL, thumb(project.img, 640))

                items.append({
                    "project": project,
                    "project_url": project_url,
                    "hive_team_members": hive_team_members,
                    "category_name": project.category.title_plural,
                    "category_url": category_url,
                    "project_image_url": project_image_url,
                })

            post_body = get_template("update_post/update_post.md").render(context={
                "items": items,
                "last_post": last_post
            })

            print(post_body)

            post = UpdatePost.objects.create(publish_date=datetime.datetime.now(), body_text=post_body)
            post.projects = projects
            post.save()

            total_projects_count = Project.objects.published().count()
            new_projects_count = len(projects)

            self.publish_update_post(post, new_projects_count, total_projects_count, post_body)

        else:
            print('No new posts to publish report, skipping')


    @staticmethod
    def publish_update_post(post, new_projects_count, total_projects_count, post_body):
        permlink = 'hiveprojects-weekly-update-' + str(datetime.date.today()) +  '-' + ''.join(random.choices(string.digits, k=5))
        link = "/@" + settings.HIVE_ACCOUNT + "/" + permlink
        title = "Hive Projects update: %d projects added, %s listed in total!" % (new_projects_count, total_projects_count)
        beneficiaries = [{'account': settings.UPDATE_POST_BENEFICIARY, 'weight': int(settings.UPDATE_POST_BENEFICIARY_WEIGHT)}]

        post.link = link
        post.title = title
        post.save()

        if settings.HIVE_NODES:
            client = Hive(node=settings.HIVE_NODES, keys=[settings.HIVE_POSTING_KEY])
        else:
            client = Hive(keys=[settings.HIVE_POSTING_KEY])

        client.post(
            permlink=permlink,
            title=title,
            body=post_body,
            author=settings.HIVE_ACCOUNT,
            tags=settings.UPDATE_POST_TAGS,
            beneficiaries=beneficiaries,
            percent_hbd=0,
            percent_steem_dollars=0)

        print('Post published successfully', title)
