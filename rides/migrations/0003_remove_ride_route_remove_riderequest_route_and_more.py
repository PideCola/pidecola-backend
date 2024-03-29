# Generated by Django 5.0.2 on 2024-03-07 15:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0002_riderequest_ride'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ride',
            name='route',
        ),
        migrations.RemoveField(
            model_name='riderequest',
            name='route',
        ),
        migrations.AddField(
            model_name='riderequest',
            name='destination',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.DO_NOTHING, related_name='ride_destination', to='rides.route'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='riderequest',
            name='origin',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.DO_NOTHING, related_name='ride_origin', to='rides.route'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ride',
            name='status',
            field=models.CharField(choices=[('pending', 'Pendiente'), ('started', 'Iniciado'), ('finished', 'Finalizado')], default='pending', max_length=16),
        ),
    ]
