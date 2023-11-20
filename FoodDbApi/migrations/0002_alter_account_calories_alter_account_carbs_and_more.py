# Generated by Django 4.2.7 on 2023-11-09 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FoodDbApi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='calories',
            field=models.FloatField(default=2400),
        ),
        migrations.AlterField(
            model_name='account',
            name='carbs',
            field=models.FloatField(default=200),
        ),
        migrations.AlterField(
            model_name='account',
            name='fat',
            field=models.FloatField(default=60),
        ),
        migrations.AlterField(
            model_name='account',
            name='protein',
            field=models.FloatField(default=90),
        ),
    ]
