# Generated by Django 4.2.7 on 2023-11-10 22:33

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('last_reset', models.CharField(max_length=10)),
                ('daily_streak', models.IntegerField(default=0)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=255)),
                ('height', models.FloatField()),
                ('weight', models.FloatField()),
                ('activitylevel', models.IntegerField()),
                ('goal', models.CharField(max_length=255)),
                ('calories', models.FloatField()),
                ('protein', models.FloatField()),
                ('fat', models.FloatField()),
                ('carbs', models.FloatField()),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daily_streak', models.BooleanField(default=True)),
                ('macro_colors', models.CharField(default='normal', max_length=15)),
                ('calories', models.BooleanField(default=True)),
                ('protein', models.BooleanField(default=True)),
                ('fat', models.BooleanField(default=False)),
                ('carbs', models.BooleanField(default=True)),
                ('nutrients_per_meal', models.BooleanField(default=True)),
                ('meals_view', models.CharField(default='normal', max_length=15)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NutritionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('grams', models.FloatField(default=0.0)),
                ('icon_name', models.CharField(default='food-fork-drink', max_length=50)),
                ('cal', models.FloatField(default=0.0)),
                ('prot', models.FloatField(default=0.0)),
                ('fat', models.FloatField(default=0.0)),
                ('chol', models.FloatField(default=0.0)),
                ('sod', models.FloatField(default=0.0)),
                ('carb', models.FloatField(default=0.0)),
                ('sugars', models.FloatField(default=0.0)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FoodModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal', models.CharField(max_length=20)),
                ('grams', models.FloatField(default=0.0)),
                ('cal', models.FloatField(default=0.0)),
                ('prot', models.FloatField(default=0.0)),
                ('fat', models.FloatField(default=0.0)),
                ('chol', models.FloatField(default=0.0)),
                ('sod', models.FloatField(default=0.0)),
                ('carb', models.FloatField(default=0.0)),
                ('sugars', models.FloatField(default=0.0)),
                ('nutrition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FoodDbApi.nutritionmodel')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
