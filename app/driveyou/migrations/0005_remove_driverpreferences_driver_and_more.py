# Generated by Django 4.2.7 on 2023-12-08 01:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('driveyou', '0004_searchrequest_distance_searchrequest_duration_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driverpreferences',
            name='driver',
        ),
        migrations.AddField(
            model_name='searchrequest',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='searchrequest',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='earnings',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='is_client',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_driver',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='licence_verification_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='location_lat',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='location_lon',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='searchrequest',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='Driver',
        ),
        migrations.DeleteModel(
            name='DriverPreferences',
        ),
    ]