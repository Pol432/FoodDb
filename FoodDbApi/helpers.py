from .models import Account, FoodModel

from django.db.models import Sum
from datetime import datetime


def reset_daily(user_id):
    # Getting account data and today's date
    account = Account.objects.get(id=user_id)
    last_reset = datetime.strptime(account.last_reset, "%d/%m/%Y")
    today = datetime.now()

    # If it isn't the next day then return
    if not last_reset.date() < today.date():
        account.save()
        return

    # Calculate the total sums for cal, prot, fat, and carb fields
    total_cal = FoodModel.objects.aggregate(Sum('cal'))['cal__sum'] or 0
    total_prot = FoodModel.objects.aggregate(Sum('prot'))['prot__sum'] or 0
    total_fat = FoodModel.objects.aggregate(Sum('fat'))['fat__sum'] or 0
    total_carb = FoodModel.objects.aggregate(Sum('carb'))['carb__sum'] or 0

    account.last_reset = today.strftime("%d/%m/%Y")
    food_records = FoodModel.objects.all()
    for food in food_records:
        food.grams = 0.0
        food.cal = 0.0
        food.prot = 0.0
        food.fat = 0.0
        food.chol = 0.0
        food.sod = 0.0
        food.carb = 0.0
        food.sugars = 0.0
        food.save()

    # Calculate the 10% range for each account field
    cal_range = 0.10 * account.calories
    prot_range = 0.10 * account.protein
    fat_range = 0.10 * account.fat
    carb_range = 0.10 * account.carbs

    # Check if the calculated totals are within the 10% range of the account fields
    if (
        (account.calories - cal_range <= total_cal <= account.calories + cal_range) and
        (account.protein - prot_range <= total_prot <= account.protein + prot_range) and
        (account.fat - fat_range <= total_fat <= account.fat + fat_range) and
        (account.carbs - carb_range <= total_carb <= account.carbs + carb_range)
    ):
        account.daily_streak += 1
    else:
        account.daily_streak = 0

    account.save()
