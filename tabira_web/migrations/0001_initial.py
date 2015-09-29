# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deviation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deviation_id', models.CharField(max_length=38)),
                ('da_url', models.URLField(default=b'')),
                ('fav_me_url', models.URLField(default=b'', blank=True)),
                ('title', models.CharField(max_length=80)),
                ('author_name', models.CharField(max_length=20)),
                ('author_id', models.CharField(max_length=38)),
                ('timestamp', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=8)),
                ('name', models.CharField(max_length=40)),
                ('image', models.CharField(default=b'', max_length=20, blank=True)),
                ('active', models.BooleanField(default=False)),
                ('timestamp', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'', max_length=20, blank=True)),
                ('status', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('folder_id', models.CharField(max_length=36)),
                ('parent', models.CharField(default=b'', max_length=36, null=True, blank=True)),
                ('name', models.CharField(max_length=80)),
                ('monitor', models.BooleanField(default=False, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Logbook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('custom_name', models.CharField(default=b'', max_length=80, blank=True)),
                ('order', models.IntegerField(default=9999)),
                ('deviation', models.ForeignKey(blank=True, to='tabira_web.Deviation', null=True)),
                ('event', models.ForeignKey(to='tabira_web.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'Active', max_length=20)),
                ('species', models.IntegerField()),
                ('species_line', models.IntegerField()),
                ('shiny', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=80)),
                ('gender', models.CharField(default=b'', max_length=20, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('joined', models.DateField()),
                ('favor_earned', models.IntegerField(default=0)),
                ('favor_spent', models.IntegerField(default=0)),
                ('rep_keepers', models.IntegerField(default=0)),
                ('rep_trackers', models.IntegerField(default=0)),
                ('rep_scholars', models.IntegerField(default=0)),
                ('rep_artisans', models.IntegerField(default=0)),
                ('cameos', models.CharField(default=b'No', max_length=12)),
                ('type', models.CharField(default=b'Drawn', max_length=12, blank=True)),
                ('tumblr', models.URLField(default=b'', blank=True)),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=50)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=20, db_index=True)),
                ('icon', models.CharField(default=b'', max_length=70)),
                ('ip', models.GenericIPAddressField(default=b'')),
                ('admin', models.BooleanField(default=False)),
                ('beta', models.BooleanField(default=False)),
                ('da_id', models.CharField(max_length=38)),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='authors',
            field=models.ManyToManyField(related_name='team_id', to='tabira_web.User'),
        ),
        migrations.AddField(
            model_name='team',
            name='logbooks',
            field=models.ManyToManyField(related_name='team_id', to='tabira_web.Logbook'),
        ),
        migrations.AddField(
            model_name='team',
            name='teammates',
            field=models.ManyToManyField(related_name='team_id', to='tabira_web.Pokemon'),
        ),
        migrations.AddField(
            model_name='feed',
            name='team',
            field=models.ForeignKey(to='tabira_web.Team'),
        ),
        migrations.AddField(
            model_name='feed',
            name='user',
            field=models.ForeignKey(to='tabira_web.User'),
        ),
        migrations.AddField(
            model_name='event',
            name='folder',
            field=models.ForeignKey(to='tabira_web.Gallery', null=True),
        ),
        migrations.AddField(
            model_name='deviation',
            name='gallery',
            field=models.ForeignKey(to='tabira_web.Gallery'),
        ),
    ]
