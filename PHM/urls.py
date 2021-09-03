from django.contrib import admin
from django.urls import path
from PHM.views import *
from User.views import *
from django.urls import include

app_name = 'phm'
urlpatterns = [
    path('upData/', upData, name="upData"),
    path('getData/', getNowData, name="getData"),
    path('getDataByTime/', getDataByTime, name="getDataByTime"),
    path('getFile/', getFile, name = "getFile"),
    path('faultDiagnosis/',faultDiagnosis,name="faultDiagnosis"),
    path('test/',test,name="test"),
]