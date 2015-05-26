# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('oga_webapi', '0002_auto_20150519_2018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gaitsample',
            name='file_name',
        ),
        migrations.AddField(
            model_name='gaitsample',
            name='gait_file',
            field=models.FileField(default=datetime.datetime(2015, 5, 21, 20, 42, 1, 556111, tzinfo=utc), upload_to=b'gait_files'),
            preserve_default=False,
        ),
    ]
