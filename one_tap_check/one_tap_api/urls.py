from django.urls import path
from .views.create_session_api_view import CreateSessionApiView
from .views.attend_session_api_view import AttendSessionApiView
from .views.end_session_view import EndSessionApiView

urlpatterns = [
    path('attendance/create', CreateSessionApiView),
    path('attendance/attend', AttendSessionApiView),
    path('attendance/end', EndSessionApiView)
]
