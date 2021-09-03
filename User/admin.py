from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name','nickname', 'pass_word', 'phone',
                    'gender', 'info', 'isLogin', 'cookie', 'token')
    fields = ('name','nickname', 'pass_word', 'phone',
                    'gender', 'info', 'isLogin', 'cookie', 'token')