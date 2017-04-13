# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0003_currency'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Currency',
        ),
    ]
