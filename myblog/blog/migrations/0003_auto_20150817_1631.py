# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='usrname',
            new_name='username',
        ),
    ]
