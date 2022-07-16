from django.contrib import admin
from django.urls import path, include
from .views import firstTournament, secondTournament, thirdTournament, loginPage, sendCode, checkCode, tournament, submitAnswer

urlpatterns = [
    path('adminDashboard/first/<int:page>', firstTournament, name="firstT"),
    path('adminDashboard/second/<int:page>', secondTournament, name="secondT"),
    path('adminDashboard/third/<int:page>', thirdTournament, name="thirdT"),
    path('', loginPage),
    path('login', loginPage),
    path('challenge/sendCode', sendCode),
    path('challenge/resendCode', sendCode),
    path('challenge/checkCode', checkCode),
    path('questions', tournament),
    path('submitanswer', submitAnswer),
]
