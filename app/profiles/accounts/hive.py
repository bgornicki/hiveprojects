from django.conf import settings
from hive import Hive


class HiveHandler(object):

    def __init__(self):
        if settings.HIVE_NODES:
            self.hive = Hive(nodes=settings.HIVE_NODES)
        else:
            self.hive = Hive()

    def get_account(self, name):
        return self.hive.get_account(name)


account_handler = HiveHandler()
