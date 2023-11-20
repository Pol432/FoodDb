from django.urls import path
from .views import (
    UserRegister,
    UserLogin,
    UserLogout,
    NutritionManagement,
    FoodManagement,
    AccountManagement,
    SettingsManagement,
)

urlpatterns = [
    path('register', UserRegister.as_view(), name='register'),
    path('login', UserLogin.as_view(), name='login'),
    path('logout', UserLogout.as_view(), name='logout'),
    path('nutrition/<int:food_id>', NutritionManagement.as_view()),
    path('food/<str:meal>/<int:food_id>', FoodManagement.as_view()),
    path('settings', SettingsManagement.as_view()),
    path('account', AccountManagement.as_view()),
]
