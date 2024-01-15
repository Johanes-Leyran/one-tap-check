from django.shortcuts import render
from .models import Attendance

# Create your views here.

def attendance_detail(request, attendance_id):
    attendance = Attendance.objects.get(id=attendance_id)
    
    return render(request, 'room101.html', {'attendance': attendance})