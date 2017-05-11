# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-11 15:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('materiaux', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brouillon',
            fields=[
                ('materiau_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='materiaux.Materiau')),
            ],
            bases=('materiaux.materiau',),
        ),
    ]