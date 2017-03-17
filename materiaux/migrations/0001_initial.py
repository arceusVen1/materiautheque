# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-17 22:23
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matiere', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=4, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Materiau',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(default='00', max_length=255, unique=True, verbose_name='référence')),
                ('nom', models.CharField(default='N.R.', max_length=255, verbose_name='Nom générique')),
                ('fournisseur', models.CharField(default='N.R.', max_length=255)),
                ('usage', models.TextField(default='N.R.')),
                ('date', models.DateField(auto_now_add=True)),
                ('disponible', models.BooleanField(default=True, verbose_name='Disponibilité')),
                ('normatif', models.CharField(choices=[('NR', 'N.R'), ('ECO', 'écolo')], default=(0, 'N.R.'), max_length=255, verbose_name='Critère normatif')),
                ('proprietes', models.TextField(default='{}', null=True, verbose_name='Propriétés')),
                ('qrcode', models.ImageField(default=None, null=True, upload_to='materiaux')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=6, unique=True)),
                ('matiere', models.CharField(max_length=255)),
                ('famille', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materiaux.Famille')),
            ],
        ),
        migrations.AddField(
            model_name='materiau',
            name='ss_famille',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materiaux.SousFamille', verbose_name='Sous-famille'),
        ),
    ]
