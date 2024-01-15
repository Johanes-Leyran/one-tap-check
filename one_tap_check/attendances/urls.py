from django.urls import path
from .views import attendance_detail

urlpatterns = [
    path('view/<int:attendance_id>/', attendance_detail, name="attendance-detail"),
]