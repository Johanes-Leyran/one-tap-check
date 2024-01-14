from django.urls import path
from . import views

urlpatterns = [
    path('tap-in/', views.RoomTapInView.as_view(), name='tap-in'),
]