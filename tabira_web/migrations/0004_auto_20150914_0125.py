# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tabira_web', '0003_item_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='folder',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='custom_name',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='custom_url',
        ),
        migrations.AddField(
            model_name='event',
            name='order',
            field=models.IntegerField(default=999),
        ),
    ]
