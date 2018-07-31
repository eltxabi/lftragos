# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alineacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dinero', models.IntegerField()),
                ('puntos_iniciales', models.IntegerField(default=0)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Futbolista',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=30)),
                ('posicion', models.CharField(max_length=3, choices=[(b'POR', b'Portero'), (b'DEF', b'Defensa'), (b'MED', b'Medio'), (b'DEL', b'Delantero')])),
                ('club', models.CharField(max_length=20)),
                ('precio', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Jornada',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField(unique=True)),
                ('limite', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Puntuacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('puntos', models.IntegerField(null=True)),
                ('futbolista', models.ManyToManyField(to='lftragos.Futbolista')),
                ('jornada', models.ManyToManyField(to='lftragos.Jornada')),
            ],
        ),
        migrations.AddField(
            model_name='alineacion',
            name='equipo',
            field=models.ManyToManyField(to='lftragos.Equipo'),
        ),
        migrations.AddField(
            model_name='alineacion',
            name='futbolista',
            field=models.ManyToManyField(to='lftragos.Futbolista'),
        ),
        migrations.AddField(
            model_name='alineacion',
            name='jornada',
            field=models.ManyToManyField(to='lftragos.Jornada'),
        ),
    ]
