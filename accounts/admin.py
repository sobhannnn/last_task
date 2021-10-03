from django.apps import apps
from django.contrib import admin
from django.forms import models
# from mptt.admin import MPTTModelAdmin
from .models import MyUser, Otp
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password', 'melli_code', 'code', 'phone_number', 'age', 'roles', 'first_name',
#                   'last_name')


# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password', 'melli_code', 'code', 'phone_number', 'age', 'roles', 'first_name',
#                   'last_name')


class MyUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'location', 'date_of_birth')}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'location', 'date_of_birth')}),
    )
    model = MyUser
    # list_display = ['id', 'username', 'melli_code', 'first_name', 'last_name']


admin.site.register(MyUser, MyUserAdmin)



class OtpAdmin(admin.ModelAdmin):
    models = Otp
    fields = ('user', 'is_verify', 'code')

admin.site.register(Otp, OtpAdmin)