from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from schedules.models.schedule_unit import ScheduleUnit
from schedules.models.schedule_sheet import ScheduleSheet
from profiles.models.section import Section
from attendances.models.attendance import Attendance
import calendar
from django.http import JsonResponse


def home_page(request):
    return render(request, 'dashboard/home_page.html')


@login_required
def dashboard_teacher(request, pk):
    user_id = pk
    user_model = get_user_model()
    user = user_model.objects.get(pk=user_id)

    if user.has_perm('accounts.set_teacher_status'):
        # get the schedule this day of the week
        current_date = timezone.localtime(timezone.now())
        current_day_week = calendar.day_name[current_date.weekday()]
        schedule_sheet = ScheduleSheet.objects.filter(users=user)
        current_units = []

        for sched in schedule_sheet:
            for unit in sched.schedule_units.filter(at_day=current_day_week):
                current_units.append(unit)

        data = {
            'profile': user.teacher_profile,
            'current_units': current_units,
            'current_date': current_date.strftime('%A - %B - %Y'),
        }

        return render(request, 'dashboard/teacher/dashboard.html', data)


def dashboard_teacher_class_list(request, pk):
    user_id = pk
    user_model = get_user_model()
    user = user_model.objects.get(pk=user_id)

    if user.has_perm('accounts.set_teacher_status'):
        # get all the section that is associated to the teacher
        teacher_profile = user.teacher_profile

        if not teacher_profile:
            data = {
                'error_message': "This account has no teacher profile"
            }
            return render(request, 'generic_error.html', data)

        data = {
            'profile': user.teacher_profile,
            'sections': 'section'
        }

        return render(request, 'dashboard/teacher/classlist.html', context=data)


def attendance_list(request, pk):
    user_id = pk

    user_model = get_user_model()
    user = user_model.objects.get(pk=user_id)

    if user.has_perm('accounts.set_teacher_status'):

        data = {
            "user": user,
            "attendances": user.attendance_records.all()
        }

        return render(request, 'dashboard/teacher/attendance_list.html', context=data)


def attendance(request, pk, at_pk):
    user_id = pk
    attendance_id = at_pk

    user_model = get_user_model()
    user = user_model.objects.get(pk=user_id)

    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # If the request is AJAX, return JSON response
        attendance_record = Attendance.objects.get(pk=attendance_id)

        data = {
            'attendance': attendance_record
        }

        return JsonResponse(data)

    if user.has_perm('accounts.set_teacher_status'):
        attendance_record = Attendance.objects.get(pk=attendance_id)

        if not attendance_record:
            data = {
                'error_message': "No attendance found"
            }
            return render(request, 'generic_error.html', data)

        data = {
            'attendance': attendance_record
        }



        return render(request, 'dashboard/teacher/attendance_record.html', context=data)