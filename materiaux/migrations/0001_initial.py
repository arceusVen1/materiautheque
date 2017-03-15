# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 20:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Famille',
            fields=[
                ('matiere', models.CharField(max_length=255)),
                ('abrege', models.CharField(max_length=4, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Materiau',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=255, unique=True)),
                ('fournisseur', models.CharField(default='N.R.', max_length=255)),
                ('usage', models.TextField(default='N.R.')),
                ('date', models.DateField(auto_now_add=True)),
                ('disponible', models.BooleanField(default=True, verbose_name='Disponibilité')),
                ('normatif', models.CharField(choices=[(0, 'N.R'), (1, 'écolo')], default=(0, 'N.R.'), max_length=255, verbose_name='Critère normatif')),
                ('famille', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materiaux.Famille')),
            ],
            options={
                'verbose_name': 'Materiau',
                'verbose_name_plural': 'Materiaux',
            },
        ),
        migrations.CreateModel(
            name='SousFamille',
            fields=[
                ('reference', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('matiere', models.CharField(max_length=255)),
                ('numero', models.IntegerField()),
                ('famille', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materiaux.Famille')),
            ],
        ),
        migrations.AddField(
            model_name='materiau',
            name='ss_famille',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materiaux.SousFamille', verbose_name='Sous-famille'),
        ),
    ]