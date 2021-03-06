# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-17 23:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Propriete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=255, unique=True, verbose_name='Nom')),
                ('unite', models.CharField(default='N.R.', max_length=30, verbose_name='Unité')),
                ('definition', models.TextField(default='N.R.')),
            ],
            options={
                'verbose_name': 'Propriété',
                'verbose_name_plural': 'Propriétés',
            },
        ),
    ]
