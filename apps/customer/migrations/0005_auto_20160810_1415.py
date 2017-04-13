# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20160810_1412'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='email',
            options={'verbose_name_plural': 'Emails', 'verbose_name': 'Email'},
        ),
    ]
