# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0009_auto_20160808_0046'),
    ]

    operations = [
        migrations.CreateModel(
            name='CnCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('path', models.CharField(unique=True, max_length=255)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(db_index=True, verbose_name='Name', max_length=255)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('image', models.ImageField(null=True, verbose_name='Image', blank=True, max_length=255, upload_to='categories')),
                ('slug', models.SlugField(verbose_name='Slug', max_length=255)),
            ],
            options={
                'verbose_name': 'CnCategory',
                'ordering': ['path'],
            },
        ),
        migrations.CreateModel(
            name='EnCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('path', models.CharField(unique=True, max_length=255)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(db_index=True, verbose_name='Name', max_length=255)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('image', models.ImageField(null=True, verbose_name='Image', blank=True, max_length=255, upload_to='categories')),
                ('slug', models.SlugField(verbose_name='Slug', max_length=255)),
            ],
            options={
                'verbose_name': 'EnCategory',
                'ordering': ['path'],
            },
        ),
        migrations.RemoveField(
            model_name='category',
            name='cn_description',
        ),
        migrations.RemoveField(
            model_name='category',
            name='cn_name',
        ),
    ]
