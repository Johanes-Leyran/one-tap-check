from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('teacher/<str:pk>', views.dashboard_teacher, name='teacher_dashboard'),
    path('teacher/<str:pk>/class-list', views.dashboard_teacher_class_list, name='teacher_class_list'),
    path('teacher/<str:pk>/attendance/', views.attendance_list, name='attendance_list'),
    path('teacher/<str:pk>/attendance/<str:at_pk>', views.attendance, name="attendance_view")
]
