from django.urls import path
from . import views

urlpatterns = [
    path('teacher/<str:pk>', views.dashboard_teacher, name='teacher_dashboard'),
    path('teacher/<str:pk>/section/list/', views.section_list, name='teacher_section_list'),
    path('teacher/<str:pk>/section/view/<str:name>', views.section_view, name='teacher_section_view'),
    path('teacher/<str:pk>/schedules/list', views.schedules, name='teacher_schedules_list'),
    path('teacher/<str:pk>/attendance/list/<str:section>', views.attendance_list, name='teacher_attendance_list'),
    path('teacher/<str:pk>/attendance/view/<str:at_pk>', views.attendance, name="teacher_attendance_view"),
]
