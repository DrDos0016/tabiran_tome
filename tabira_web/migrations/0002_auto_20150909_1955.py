# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tabira_web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('custom_name', models.CharField(max_length=70)),
                ('custom_url', models.URLField(default=b'', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('image', models.CharField(max_length=40)),
                ('url', models.URLField(default=b'http://www.talesoftabira.com/wiki/Items', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='inventory',
            name='item',
            field=models.ForeignKey(to='tabira_web.Item'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='team',
            field=models.ForeignKey(to='tabira_web.Team'),
        ),
    ]
