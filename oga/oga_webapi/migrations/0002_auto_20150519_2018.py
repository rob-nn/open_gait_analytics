# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oga_webapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GaitCycle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripton', models.CharField(max_length=50)),
                ('initial_contact_frame', models.PositiveIntegerField()),
                ('end_terminal_swing_frame', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='GaitSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('file_name', models.FileField(upload_to=b'')),
                ('patient', models.ForeignKey(related_name='samples', to='oga_webapi.Patient')),
            ],
        ),
        migrations.AddField(
            model_name='gaitcycle',
            name='gait_sample',
            field=models.ForeignKey(to='oga_webapi.GaitSample'),
        ),
    ]
