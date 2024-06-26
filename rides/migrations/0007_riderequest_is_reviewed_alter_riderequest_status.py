# Generated by Django 5.0.2 on 2024-04-01 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0006_ride_destination_ride_origin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='riderequest',
            name='is_reviewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='riderequest',
            name='status',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('aceptado', 'Aceptado'), ('iniciado', 'Iniciado'), ('finalizado', 'Finalizado'), ('cancelado', 'Cancelado')], default='pendiente', max_length=16),
        ),
    ]
