from django.core.management.base import BaseCommand

from newsletter.services import NewsletterSender


class Command(BaseCommand):
    help = 'tbd'

    def handle(self, *args, **kwargs):
        NewsletterSender()
