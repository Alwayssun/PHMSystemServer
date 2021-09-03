
from django.contrib import admin
from django.urls import path
from .views import *
app_name = 'user'

urlpatterns = [
    path('emailVerify/', emailVerify, name="emailVerify"),
    path('emailVerifyVerify/', emailVerifyVerify, name="emailVerifyVerify"),
    path('signUp/', signUp, name="signUp"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('getInfo/',getInfo,name='getInfo'),
    path('changeInfo/',changeInfo,name='changeInfo'),
    path('changePassword/', changePassage, name='changePassage'),
    path('uploadIcon/', uploadIcon, name = 'uploadIcon'),
    path('getIcon/', getIcon, name = 'getIcon'),

]

