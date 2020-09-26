import textwrap

from django.conf import settings

from rocketchat_API.rocketchat import RocketChat

from package.models import TeamMembership
from profiles.models import Account

try:
    from django.core.management.base import NoArgsCommand
except ImportError:
    from django.core.management import BaseCommand as NoArgsCommand


class Command(NoArgsCommand):
    help = "Send messages via openhive.chat"

    def handle(self, *args, **options):

        proxyDict = {}

        rocket = RocketChat(
            settings.ROCKET_CHAT_LOGIN,
            settings.ROCKET_CHAT_PASSWORD,
            server_url=settings.ROCKET_CHAT_URL,
            proxies=proxyDict
        )

        template = textwrap.dedent(
            """
            Hello {name} :) !

            I would like to let you know, that you are added as a team-member to {project_plular} which {project_be} listed now on brand new [HiveProjects.com](https://HiveProjects.com/) :) List of all your known project user will be able to find on your profile page: {profile_page}

            What is a HiveProjects? If you are familiar with HiveTools, then think about it as better version of it :) Big difference is that HiveProjects is a community driven website. **You as a project member can add/modify information about your projects**.

            HiveProjects is now in pre-release stage. It is now time to make sure, that all your Hive-related projects are added to database and are in the good shape. Here is a list of all your project which I know about:
            """
        )

        accounts = []

        for account in Account.objects.filter(account_type__name='HIVE'):
            if not account.profile:
                accounts.append((account,))
            else:
                accounts.append(list(account.profile.account_set.all()))

        for accounts_tuple in accounts:

            membership = TeamMembership.objects.filter(account__in=accounts_tuple)
            if not membership.exists():
                continue

            hive_name = accounts_tuple[0].name if not accounts_tuple[0].profile else accounts_tuple[0].profile.hive_account.name

            chat_user_info = rocket.users_info(username=hive_name).json()

            if not chat_user_info['success']:
                print("User {} do not have account on openhive.chat".format(hive_name))
                continue
            else:
                print ("User {} - ok".format(hive_name))

            many_projects = membership.count() > 1

            message = template.format(
                name=hive_name,
                profile_page="{}/@{}".format(settings.SITE_URL, hive_name),
                project_plular="{} projects".format(membership.count()) if many_projects else "a project",
                project_be="are" if many_projects else "is",

            )

            for tm in membership:
                message += "  - [{}]({})\n".format(
                    tm.project.name,
                    "{}{}".format(settings.SITE_URL, tm.project.get_absolute_url())
                )

            message += textwrap.dedent("""
                Before editing a project or adding a new one, please read the instruction first: [{instruction_title}]({instruction_url}) - otherwise a result might be far from perfect.

                In case of any question, don't hesitate to ask me! :)
                """.format(
                    instruction_title='Tutorial: How to add/edit a project on HiveProjects.com',
                    instruction_url='https://peakd.com/utopian-io/@noisy/pre-release-tutorial-how-to-add-edit-a-project-on-steemprojects-com',
                )
            )

            print("-" * 60)
            print(message)
            print("-" * 60)

            ans = input('##### Send PM to @{}? [y/n/q]: '.format(hive_name))
            if ans.lower() == 'y':
                res = rocket.chat_post_message(text=message, channel="@{}".format(hive_name))
                print(str(res.json()))
            elif ans.lower() == 'q':
                return
