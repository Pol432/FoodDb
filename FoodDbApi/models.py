from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    last_reset = models.CharField(max_length=10)
    daily_streak = models.IntegerField(default=0)

    age = models.IntegerField()
    gender = models.CharField(max_length=255)
    height = models.FloatField()
    weight = models.FloatField()

    activitylevel = models.IntegerField()
    goal = models.CharField(max_length=255)

    calories = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    carbs = models.FloatField()

    def __str__(self):
        return f"Account(username={self.username}, goal={self.goal})"


class NutritionModel(models.Model):
    name = models.CharField(max_length=25)
    grams = models.FloatField(default=0.0)
    icon_name = models.CharField(max_length=50, default="food-fork-drink")

    cal = models.FloatField(default=0.0)
    prot = models.FloatField(default=0.0)
    fat = models.FloatField(default=0.0)
    chol = models.FloatField(default=0.0)
    sod = models.FloatField(default=0.0)
    carb = models.FloatField(default=0.0)
    sugars = models.FloatField(default=0.0)

    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)


class FoodModel(models.Model):
    meal = models.CharField(max_length=20)
    grams = models.FloatField(default=0.0)

    cal = models.FloatField(default=0.0)
    prot = models.FloatField(default=0.0)
    fat = models.FloatField(default=0.0)
    chol = models.FloatField(default=0.0)
    sod = models.FloatField(default=0.0)
    carb = models.FloatField(default=0.0)
    sugars = models.FloatField(default=0.0)

    nutrition = models.ForeignKey(NutritionModel, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)


class Settings(models.Model):
    daily_streak = models.BooleanField(default=True)
    macro_colors = models.CharField(max_length=15, default="normal")

    calories = models.BooleanField(default=True)
    protein = models.BooleanField(default=True)
    fat = models.BooleanField(default=False)
    carbs = models.BooleanField(default=True)

    nutrients_per_meal = models.BooleanField(default=True)
    meals_view = models.CharField(max_length=15, default="normal")

    user_id = models.OneToOneField(Account, on_delete=models.CASCADE)
