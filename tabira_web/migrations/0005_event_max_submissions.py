# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tabira_web', '0004_auto_20150914_0125'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='max_submissions',
            field=models.IntegerField(default=1),
        ),
    ]
