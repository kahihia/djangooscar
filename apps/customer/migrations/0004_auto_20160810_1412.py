# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20160701_0833'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='email',
            options={'verbose_name_plural': 'EmailsS', 'verbose_name': 'Emails'},
        ),
    ]
