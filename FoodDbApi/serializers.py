from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .models import *

from datetime import datetime
import requests

macro_calculator_url = "https://fitness-calculator.p.rapidapi.com/macrocalculator"
macro_calculator_headers = {
    "X-RapidAPI-Key": "b6c7d1f116msh52b05cb3b3e3d7dp18bf11jsn71e2bbdfaa52",
    "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com"
}


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = Account
        exclude = ['calories', 'protein', 'fat',
                   'carbs', 'last_reset', 'daily_streak']

    def create(self, clean_data):
        querystring = {
            "age": str(clean_data["age"]),
            "gender": clean_data["gender"],
            "height": str(clean_data["height"]),
            "weight": str(clean_data["weight"]),
            "activitylevel": str(clean_data["activitylevel"]),
            "goal": clean_data["goal"],
        }

        result = requests.get(
            macro_calculator_url, headers=macro_calculator_headers, params=querystring
        ).json()["data"]

        user_obj = Account.objects.create_user(
            username=clean_data['username'],
            email=clean_data['email'],
            password=clean_data['password'],
            age=clean_data["age"],
            gender=clean_data["gender"],
            height=clean_data["height"],
            weight=clean_data["weight"],
            activitylevel=clean_data["activitylevel"],
            goal=clean_data["goal"],
            last_reset=datetime.now().strftime("%d/%m/%Y"),
            calories=result["calorie"],
            protein=result["balanced"]["protein"],
            fat=result["balanced"]["fat"],
            carbs=result["balanced"]["carbs"],
        )
        user_obj.username = clean_data['username']

        settings_obj = Settings.objects.create(
            user_id=user_obj
        )

        user_obj.save()
        settings_obj.save()
        return user_obj


class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField()
    ##

    def check_user(self, clean_data):
        user = authenticate(
            username=clean_data['username'], password=clean_data['password']
        )
        if not user:
            raise ValidationError('user not found')
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'username')


data = {"username": "Pol", "email": "pmrosero@gmail.com", "password": "123456"}


class NutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionModel
        exclude = ['user_id']


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodModel
        exclude = ['nutrition', 'user_id']


class NutritionGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionModel
        fields = '__all__'


class FoodGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodModel
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'daily_streak', 'email', 'password', 'age', 'gender', 'height', 'weight',
                  'activitylevel', 'goal', 'last_reset', 'calories', 'protein', 'fat', 'carbs']

    last_reset = serializers.DateTimeField(required=False)
    calories = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False)
    protein = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False)
    fat = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False)
    carbs = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False)


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'
