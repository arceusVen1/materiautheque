# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-11 23:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import packs.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('materiaux', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FamillePack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=4, unique=True, verbose_name='Référence')),
            ],
        ),
        migrations.CreateModel(
            name='ImagePack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legende', models.CharField(default='', max_length=255, verbose_name='Légende')),
                ('imagefile', models.ImageField(blank=True, upload_to=packs.models.image_file_name, verbose_name='Image')),
            ],
        ),
        migrations.CreateModel(
            name='Pack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(default='00', max_length=255, unique=True, verbose_name='Référence')),
                ('nom', models.CharField(default='N.R.', max_length=255, verbose_name='Nom générique')),
                ('marque', models.CharField(default='N.R.', max_length=255, verbose_name='Marque')),
                ('procedes_employes', models.TextField(default='N.R.', verbose_name='Procédés employés')),
                ('date', models.DateField(auto_now_add=True)),
                ('normatif', models.CharField(choices=[('NR', 'N.R'), ('ECO', 'écolo')], default=(0, 'N.R.'), max_length=255, verbose_name='Critère normatif')),
                ('disponible', models.BooleanField(default=True, verbose_name='Disponibilité')),
                ('qrcode', models.ImageField(default=None, null=True, upload_to='packs')),
                ('famille', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packs.FamillePack')),
                ('materiaux_employes', models.ManyToManyField(blank=True, to='materiaux.Materiau', verbose_name='Matériaux employés')),
            ],
            options={
                'verbose_name': 'Pack',
                'verbose_name_plural': 'Packs',
            },
        ),
        migrations.CreateModel(
            name='SousFamillePack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=6, unique=True, verbose_name='Référence')),
                ('usage', models.CharField(max_length=255)),
                ('numero', models.IntegerField()),
                ('famille', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packs.FamillePack')),
            ],
        ),
        migrations.AddField(
            model_name='pack',
            name='ss_famille',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packs.SousFamillePack', verbose_name='Sous-famille'),
        ),
        migrations.AddField(
            model_name='imagepack',
            name='packs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packs.Pack', verbose_name='Pack associé'),
        ),
    ]