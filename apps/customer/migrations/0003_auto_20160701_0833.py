# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import oscar.models.fields.autoslugfield
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20150807_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communicationeventtype',
            name='code',
            field=oscar.models.fields.autoslugfield.AutoSlugField(unique=True, help_text='Code used for looking up this event programmatically', separator='_', blank=True, editable=False, populate_from='name', max_length=128, verbose_name='Code', validators=[django.core.validators.RegexValidator(regex='^[a-zA-Z_][0-9a-zA-Z_]*$', message="Code can only contain the letters a-z, A-Z, digits, and underscores, and can't start with a digit.")]),
        ),
    ]
