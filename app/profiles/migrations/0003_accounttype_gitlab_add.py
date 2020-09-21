from __future__ import unicode_literals

from django.db import migrations, models


def load_data(apps, schema_editor):
    AccountType = apps.get_model("profiles", "AccountType")

    AccountType.objects.get_or_create(
        name="GITLAB",
        display_name="Gitlab",
        social_auth_provider_name="gitlab",
        link_to_account_with_param="https://gitlab.com/{account_name}",
        link_to_avatar_with_params="https://gitlab.com/{account_name}.png?size={size}"
    )


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_accounttype_data_migration'),
    ]

    operations = [
        migrations.RunPython(load_data)
    ]
