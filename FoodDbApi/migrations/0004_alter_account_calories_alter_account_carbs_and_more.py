# Generated by Django 4.2.7 on 2023-11-12 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FoodDbApi', '0003_merge_20231112_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='calories',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='account',
            name='carbs',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='account',
            name='fat',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='account',
            name='protein',
            field=models.FloatField(),
        ),
    ]
