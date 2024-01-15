from django.urls import path
from .views import attendance_detail

urlpatterns = [
    path('<int:attendance_id>/', attendance_detail, name="attendance-detail"),
]