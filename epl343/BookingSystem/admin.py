from operator import is_
from turtle import onclick
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django import forms

from .forms import NewUserForm,UserChangeForm

from .models import years, payments, locations, Testimonial, Teaching_experience,Photo,PhotoSection

User = get_user_model()


# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = NewUserForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['email', 'first_name', 'last_name', 'admin', 'staff']
    list_filter = ['admin', 'staff']
    # For change/update user
    fieldsets = (
        ('Credentials', {'fields': ('email','password')}),
        ('Personal info', {'fields': ('first_name', 'last_name','preferred_loc', 'year', 'pay', 'is_student')}),
        ('Permissions', {'fields': ('admin','staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    # For add/new/create user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_student', 'preferred_loc', 'year', 'pay')}
        ),
    )
    search_fields = ['last_name']
    ordering = ['email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Testimonial)
admin.site.register(Teaching_experience)
admin.site.register(PhotoSection)
admin.site.register(Photo)
