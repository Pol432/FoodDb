# Generated by Django 4.2.7 on 2023-11-10 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FoodDbApi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='daily_streak',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='account',
            name='last_reset',
            field=models.CharField(max_length=10),
        ),
    ]
