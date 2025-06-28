# Directory: student_leave_system/core/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout

urlpatterns = [
    path('', views.choice_page, name='choice_page'),
    path('login/', views.choice_page, name='login'),  # Redirect to choice page
    path('login/student/', views.student_login, name='student_login'),
    path('login/teacher/', views.teacher_login, name='teacher_login'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('apply-leave/', views.apply_leave, name='apply_leave'),
    path('leave-requests/', views.manage_leave_requests, name='manage_leave_requests'),
    path('teacher/leave-requests/', views.manage_leave_requests, name='view_leave_requests'),
    path('profile/', views.profile_page, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('past-requests/', views.past_leave_requests, name='past_requests'),
]


