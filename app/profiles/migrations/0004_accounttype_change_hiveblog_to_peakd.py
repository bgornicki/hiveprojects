from __future__ import unicode_literals

from django.db import migrations, models
from profiles.models import Account

def load_data(apps, schema_editor):
    AccountType = apps.get_model("profiles", "AccountType")

    for account in AccountType.objects.filter(name=Account.TYPE_HIVE):
        account.link_to_account_with_param="https://peakd.com/@{account_name}"
        account.save()

class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_accounttype_gitlab_add'),
    ]

    operations = [
        migrations.RunPython(load_data)
    ]
