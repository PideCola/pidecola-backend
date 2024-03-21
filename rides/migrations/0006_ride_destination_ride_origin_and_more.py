# Generated by Django 5.0.2 on 2024-03-21 00:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0005_alter_ride_status_alter_riderequest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='destination',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ride_destination', to='rides.route'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ride',
            name='origin',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ride_origin', to='rides.route'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='riderequest',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='request_destination', to='rides.route'),
        ),
        migrations.AlterField(
            model_name='riderequest',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='request_origin', to='rides.route'),
        ),
    ]
