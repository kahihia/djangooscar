# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0011_auto_20160812_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description_img',
            field=models.ImageField(blank=True, null=True, verbose_name='Descriptionimg', upload_to='products', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='cn_description',
            field=models.TextField(blank=True, null=True, verbose_name='cn_Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='cn_title',
            field=models.CharField(blank=True, null=True, verbose_name='cn_Title', max_length=255),
        ),
    ]
