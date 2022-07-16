from django.contrib import admin
from django.urls import path, include
from .views import home, loginPage, sendCode, checkCode, tournament, submitAnswer

urlpatterns = [
    path('adminDashboard', home),
    path('', loginPage),
    path('login', loginPage),
    path('challenge/sendCode', sendCode),
    path('challenge/checkCode', checkCode),
    path('questions', tournament),
    path('submitanswer', submitAnswer),
]
