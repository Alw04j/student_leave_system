from django.contrib import admin
from .models import Class, CustomUser, LeaveRequest
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Form for validating Class creation in admin
class ClassAdminForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        level = cleaned_data.get('level')
        course = cleaned_data.get('course')
        year = cleaned_data.get('year')

        pg_courses = [
            'MSC-CS', 'MA-HRM', 'MCOM-FT', 'MSC-ELX', 'MSC-BT', 'MA-ENG'
        ]
        ug_courses = [
            'BCA-AI', 'BBA-AV', 'BCOM-CO', 'BCOM-FT',
            'BSC-ECT', 'BSC-BT', 'BA-ENG', 'BSW'
        ]

        if level == 'PG':
            if course in ug_courses:
                raise ValidationError("UG course selected for PG level.")
            if year not in ['1st', '2nd']:
                raise ValidationError("PG course can only be 1st or 2nd year.")
        if level == 'UG':
            if course in pg_courses:
                raise ValidationError("PG course selected for UG level.")
            if year not in ['1st', '2nd', '3rd']:
                raise ValidationError("UG course must be 1st to 3rd year.")

        return cleaned_data

# Admin for Class model
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    form = ClassAdminForm
    list_display = ('level', 'year', 'course', 'batch')
    list_filter = ('level', 'year', 'course', 'batch')

# Custom forms for user creation and change
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'is_student', 'is_teacher', 'class_id', 'profile_pic', 'phone_number')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'is_student', 'is_teacher', 'class_id', 'profile_pic', 'phone_number')

# Admin for CustomUser with password hashing and fields
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('username', 'is_student', 'is_teacher', 'class_id')
    list_filter = ('is_student', 'is_teacher', 'class_id')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ("Permissions", {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ("Roles and Info", {'fields': ('is_student', 'is_teacher', 'class_id', 'profile_pic', 'phone_number')}),
        ("Dates", {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_student', 'is_teacher', 'class_id', 'profile_pic', 'phone_number'),
        }),
    )

    search_fields = ('username',)
    ordering = ('username',)


# Admin for LeaveRequest
@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'from_date', 'to_date', 'status')
    list_filter = ('status',)
