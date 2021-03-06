# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-07 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='appuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20, unique=True)),
                ('email', models.CharField(max_length=55, unique=True)),
                ('interest', models.IntegerField(choices=[(0, 'Cycling'), (1, 'Running'), (2, 'Crossfit'), (3, 'AFL'), (4, 'Weightlifting'), (5, 'Cricket')], default=0)),
                ('age', models.IntegerField(default=18)),
                ('sex', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('political', models.IntegerField(choices=[(0, 'Conservative'), (1, 'Liberal'), (2, 'Libereterian')], default=0)),
                ('relation', models.IntegerField(choices=[(0, 'Single'), (1, 'Married'), (2, 'Parent')], default=0)),
                ('education', models.IntegerField(choices=[(0, 'Highschool'), (1, 'Undergraduate'), (2, 'Postgraduate')], default=0)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
