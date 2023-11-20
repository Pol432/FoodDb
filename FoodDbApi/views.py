from .validations import custom_validation, validate_email, validate_password
from .serializers import *
from .models import *
from .helpers import reset_daily

from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class NutritionManagement(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication,
    )
    # authentication_classes = (SessionAuthentication,)

    # Returns all rows in NutritionModel table or just a selected row if food_id is provided
    def get(self, request, food_id=None):
        reset_daily(request.user.id)
        if food_id and food_id != 0:
            try:
                nutrition = NutritionModel.objects.get(
                    id=food_id, user_id=request.user.id
                )
                serializer = NutritionGetSerializer(nutrition)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except NutritionModel.DoesNotExist:
                return Response("Food not Found", status=status.HTTP_404_NOT_FOUND)
        else:
            nutrition = NutritionModel.objects.filter(user_id=request.user.id)

            if not nutrition:
                return Response([], status=status.HTTP_200_OK)

            serializer = NutritionGetSerializer(nutrition, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # Creates a row in the Nutrition Model and their respective rows in the FoodModel for each meal provided
    def post(self, request, food_id=None):
        print("here")
        # Getting the last ID from the NutritionModel
        last_nutrition = NutritionModel.objects.order_by('-id').first()
        new_id = last_nutrition.id + 1 if last_nutrition else 1

        # Creating desired rows
        serializer = NutritionSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save(id=new_id, user_id=request.user)

            for meal_type in ["breakfast", "lunch", "dinner", "snack"]:
                food_data = FoodModel(
                    meal=meal_type, nutrition_id=new_id, user_id=request.user)
                food_data.save()
            return Response("Successfully added", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Updates a row based on the food_id argument from the NutritionModel table
    def patch(self, request, food_id):
        try:
            nutrition = NutritionModel.objects.get(
                id=food_id, user_id=request.user.id
            )
        except NutritionModel.DoesNotExist:
            return Response(None, status=status.HTTP_200_OK)

        serializer = NutritionSerializer(
            nutrition, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "Successfully updated food item N° " + str(food_id)},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Deletes a row in the NutritionModel table based on the food_id argument
    def delete(self, request, food_id):
        try:
            nutrition = NutritionModel.objects.get(
                id=food_id, user_id=request.user.id
            )
        except NutritionModel.DoesNotExist:
            return Response(None, status=status.HTTP_200_OK)

        food_data = FoodModel.objects.filter(nutrition=nutrition)
        food_data.delete()
        nutrition.delete()
        return Response({"data": "Successfully deleted food item: " + str(food_id)}, status=status.HTTP_200_OK)


class FoodManagement(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication,
    )
    # authentication_classes = (SessionAuthentication,)

    # Returns a single element if the food_id is provided, all the rows that have a specific meal if the meal is provided,
    # or all the rows in the FoodModel if none of the previous arguments is provided
    def get(self, request, meal=None, food_id=None):
        reset_daily(request.user.id)
        if food_id and food_id != 0:
            try:
                food = FoodModel.objects.get(id=food_id, user_id=request.user)
                serializer = FoodGetSerializer(food)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except FoodModel.DoesNotExist:
                return Response("Food not found", status=status.HTTP_404_NOT_FOUND)

        elif meal and meal in ["breakfast", "lunch", "snack", "dinner"]:
            foods = FoodModel.objects.filter(meal=meal, user_id=request.user)
        else:
            foods = FoodModel.objects.filter(user_id=request.user)

        if not foods:
            return Response([], status=status.HTTP_200_OK)
        serializer = FoodGetSerializer(foods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Creates a row in the Nutrition Model and their respective rows in the FoodModel for each meal provided
    def put(self, request, meal, food_id=None):
        # Getting the last ID from the FoodModel
        last_nutrition = NutritionModel.objects.order_by('-id').first()
        new_id = last_nutrition.id + 1 if last_nutrition else 1

        # Creating desired rows
        data = {"meal": meal, **request.data}
        print(data)
        serializer = FoodSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            nutrition = NutritionModel(id=new_id, user_id=request.user, **{key: request.data[key] for key in [
                "name", "grams", "cal", "prot", "fat", "chol", "sod", "carb", "sugars"]})
            nutrition.save()

            serializer.save(nutrition=nutrition, user_id=request.user, meal=meal, **{key: request.data[key] for key in [
                "grams", "cal", "prot", "fat", "chol", "sod", "carb", "sugars"]})

            return Response("Successfully added", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Updates a row in the FoodModel table based on the food_id argument
    def patch(self, request, food_id, meal=None):
        try:
            food = FoodModel.objects.get(id=food_id)
        except FoodModel.DoesNotExist:
            return Response("Food not found", status=status.HTTP_404_NOT_FOUND)

        if food.user_id.id != request.user.id:
            print("here")
            return Response("Trying to edit other user's food", status=status.HTTP_400_BAD_REQUEST)

        serializer = FoodSerializer(food, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "Successfully updated food item N° " + str(food_id)},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Deletes a row in the FoodModel table based on the food_id argument
    def delete(self, request, meal, food_id):
        try:
            food = FoodModel.objects.get(id=food_id)
        except FoodModel.DoesNotExist:
            return Response("Food not found", status=status.HTTP_404_NOT_FOUND)

        if food.user_id != request.user.id:
            return Response("Trying to edit other user's food", status=status.HTTP_400_BAD_REQUEST)

        food.delete()
        return Response({"data": "Successfully deleted food item: " + str(food_id)}, status=status.HTTP_200_OK)


class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        # clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(request.data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    ##

    def post(self, request):
        data = request.data
        # assert validate_email(data)
        # assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class AccountManagement(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication,
    )
    # authentication_classes = (SessionAuthentication,)

    # Retrieve account info endpoint
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"authenticated": False}, status=status.HTTP_200_OK)

        # reset_daily(request.user.id)
        try:
            account = Account.objects.get(id=request.user.id)
            serializer = AccountSerializer(account)
            return Response({"authenticated": True, **serializer.data}, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response("Account not found", status=status.HTTP_404_NOT_FOUND)

    # Account manipulation
    def patch(self, request):
        args = request.data
        try:
            account = Account.objects.get(id=request.user.id)
        except Account.DoesNotExist:
            return Response("Account not found", status=status.HTTP_404_NOT_FOUND)

        for field, value in args.items():
            if value is not None and value != "password":
                setattr(account, field, value)

        if "password" in args:
            account.set_password(args["password"])

        for field in ["age", "gender", "height", "weight", "activitylevel", "goal"]:
            if field in args:
                continue
            args[field] = getattr(account, field)

        querystring = {arg: str(args[arg]) for arg in [
            "age", "gender", "height", "weight", "activitylevel", "goal"]}

        # Perform macro calculation and update account data
        result = requests.get(
            macro_calculator_url, headers=macro_calculator_headers, params=querystring).json()["data"]

        account.calories = result["calorie"]
        account.protein = result["balanced"]["protein"]
        account.fat = result["balanced"]["fat"]
        account.carbs = result["balanced"]["carbs"]

        account.save()
        return Response({"data": "Successfully updated account item N° " + str(id)}, status=status.HTTP_200_OK)


class SettingsManagement(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication,
    )
    # authentication_classes = (SessionAuthentication,)

    # Retrieve settings of the user based on their ID
    def get(self, request):
        reset_daily(request.user.id)
        try:
            settings = Settings.objects.get(user_id=request.user)
            serializer = SettingsSerializer(settings)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Settings.DoesNotExist:
            return Response("Settings not found", status=status.HTTP_404_NOT_FOUND)

    # Settings update
    def patch(self, request):
        try:
            settings = Settings.objects.get(user_id=request.user)
        except Settings.DoesNotExist:
            return Response("Settings not found", status=status.HTTP_404_NOT_FOUND)

        args = request.data
        serializer = SettingsSerializer(settings, data=args, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "Successfully updated settings"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
