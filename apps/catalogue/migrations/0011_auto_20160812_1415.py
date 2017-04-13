# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0010_auto_20160809_1819'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CnCategory',
        ),
        migrations.DeleteModel(
            name='EnCategory',
        ),
        migrations.RemoveField(
            model_name='productclass',
            name='cn_name',
        ),
        migrations.AddField(
            model_name='category',
            name='cn_description',
            field=models.TextField(verbose_name='Cn Description', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name='cn_image',
            field=models.ImageField(upload_to='categories', verbose_name='Cn_Image', null=True, blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='category',
            name='cn_name',
            field=models.CharField(null=True, verbose_name='Cn Name', db_index=True, max_length=255),
        ),
        migrations.AddField(
            model_name='category',
            name='is_chinese',
            field=models.BooleanField(verbose_name='is Chinese', default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='is_chinese',
            field=models.BooleanField(verbose_name='is Chinese', default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='cn_description',
            field=models.TextField(verbose_name='Description', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='cn_title',
            field=models.CharField(verbose_name='Title', null=True, blank=True, max_length=255),
        ),
    ]
