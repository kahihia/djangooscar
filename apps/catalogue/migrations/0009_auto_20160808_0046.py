# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0008_auto_20160304_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cn_description',
            field=models.TextField(blank=True, verbose_name='CnDescription'),
        ),
        migrations.AddField(
            model_name='category',
            name='cn_name',
            field=models.CharField(max_length=255, verbose_name='Name', default=datetime.datetime(2016, 8, 8, 0, 46, 43, 428465, tzinfo=utc), db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='cn_description',
            field=models.TextField(blank=True, verbose_name='Cn_Description'),
        ),
        migrations.AddField(
            model_name='product',
            name='cn_title',
            field=models.CharField(blank=True, verbose_name='Cn_Title', max_length=255),
        ),
        migrations.AddField(
            model_name='productclass',
            name='cn_name',
            field=models.CharField(max_length=128, verbose_name='CnName', default=datetime.datetime(2016, 8, 8, 0, 46, 49, 100161, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
