from django.urls import path
from .views import attendances

urlpatterns = [
    path('attendance/create/', attendances.create_attendance),
    path('attendance/attend/', attendances.attend_attendance),
    path('attendance/end/', attendances.end_attendance),
    # path('attendance/delete-list', attendances.delete_list),
    # path('attendance/edit, attendances.edit,
    # path('')
]
