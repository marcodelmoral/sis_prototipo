from django.contrib.postgres.operations import CreateExtension, HStoreExtension, UnaccentExtension
from django.db import migrations


class Migration(migrations.Migration):
    run_before = [
        ('geo', '0001_initial'),
        ]

    operations = [
        HStoreExtension(),
        UnaccentExtension(),
        CreateExtension('postgis'),
        ]
