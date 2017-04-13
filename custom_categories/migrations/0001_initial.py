# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WirelessReservation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100, verbose_name='Name(passport)')),
                ('user_email', models.EmailField(max_length=100, verbose_name='E-mail')),
                ('meet_place', models.CharField(choices=[('홍대', '홍대(Hongdae)'), ('강남', '강남(Gangnam)'), ('여의도', '여의도(Yeouido)')], max_length=20, verbose_name='Place')),
                ('meet_date', models.DateField(verbose_name='Date')),
                ('meet_time', models.TimeField(verbose_name='Time')),
                ('recommended_user_email', models.EmailField(blank=True, null=True, max_length=200, verbose_name='Recommended ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('recommended_user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, related_name='recommended_wireless')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, related_name='wireless_reservation', verbose_name='WirelessReserve')),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
    ]
