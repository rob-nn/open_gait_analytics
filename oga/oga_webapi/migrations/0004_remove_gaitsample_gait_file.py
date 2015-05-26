# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oga_webapi', '0003_auto_20150521_2042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gaitsample',
            name='gait_file',
        ),
    ]
