from operator import is_
from turtle import onclick
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django import forms

from .forms import NewUserForm

from .models import years, payments, locations

User = get_user_model()

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = forms.CharField()
    is_student = forms.BooleanField(required=False)
    preferred_loc = forms.ChoiceField(choices=locations.choices)
    year = forms.ChoiceField(choices=years.choices)
    pay = forms.ChoiceField(choices=payments.choices)

   
    def is_valid(self):
        from django.core.exceptions import ValidationError
        valid = super(UserChangeForm, self).is_valid()
        loc = self.cleaned_data['preferred_loc']
        year = self.cleaned_data['year']    
        pay = self.cleaned_data['pay']
        student = self.cleaned_data['is_student']
        if student == False:
            if year==loc==pay=='NA':
                return True
            else:
                if year!='NA':
                    self.add_error('year', ValidationError('This user is not a student'))
                if loc!='NA':
                    self.add_error('preferred_loc', ValidationError('This user is not a student'))
                if pay!='NA':
                    self.add_error('pay', ValidationError('This user is not a student'))
                return False
        else:
            if year=='NA' or loc=='NA' or pay=='NA':
                if year=='NA':
                    self.add_error('year', ValidationError('This user is a student'))
                if loc=='NA':
                    self.add_error('preferred_loc', ValidationError('This user is a student'))
                if pay=='NA':
                    self.add_error('pay', ValidationError('This user is a student'))
                return False
        return True

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
        ('Credentials', {'fields': ('email', 'username','password')}),
        ('Personal info', {'fields': ('first_name', 'last_name','preferred_loc', 'year', 'pay', 'is_student')}),
        ('Permissions', {'fields': ('admin','staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    # For add/new/create user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'is_student', 'preferred_loc', 'year', 'pay')}
        ),
    )
    search_fields = ['last_name']
    ordering = ['email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
