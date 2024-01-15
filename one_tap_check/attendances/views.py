from django.shortcuts import render
from .models import Attendance

# Create your views here.

def attendance_detail(request, id):
    attendance = Attendance.objects.get(id=id)
    
    return render(request, 'attendance_detail.html', {'attendance': attendance})