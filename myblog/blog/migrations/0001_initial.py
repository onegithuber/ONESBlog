# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleScrap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=50)),
                ('title_zh', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=30)),
                ('content_md', models.TextField()),
                ('content_html', models.TextField()),
                ('tags', models.CharField(max_length=30)),
                ('views', models.IntegerField()),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
            ],
        ),
    ]
