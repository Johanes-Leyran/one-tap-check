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

        try:
            schedule_sheet = ScheduleSheet.objects.get(user=user)
        except ScheduleSheet.DoesNotExist:
            schedule_sheet = None

        current_units = []

        if schedule_sheet:
            for unit in schedule_sheet.schedule_units.filter(at_day=current_day_week):
                current_units.append(unit)

        data = {
            'user': user,
            'current_units': current_units,
            'current_date': current_date.strftime('%A - %B - %Y | %D'),
        }

        return render(request, 'dashboard/teacher/dashboard.html', data)


@login_required
def schedules(request, pk):
    user_id = pk
    user_model = get_user_model()
    user = user_model.objects.get(pk=user_id)

    if user.has_perm('accounts.set_teacher_status'):

        try:
            schedule_sheet = ScheduleSheet.objects.get(user=user)
            units = schedule_sheet.schedule_units
        except ScheduleSheet.DoesNotExist:
            schedule_sheet = None
            units = None

        data = {
            'user': user,
            'units': units
        }

        return render(request, 'dashboard/teacher/schedule_unit_list.html', data)


@login_required
def section_list(request, pk):
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

        sections = teacher_profile.sections.all()

        data = {
            'user': user,
            'sections': sections
        }

        return render(request, 'dashboard/teacher/section_list.html', context=data)


@login_required
def section_view(request, pk, name):
    user_id = pk

    user_model = get_user_model()
    user = user_model.objects.get(pk=user_id)

    if user.has_perm('accounts.set_teacher_status'):
        section = Section.objects.get(pk=name)

        data = {
            'user': user,
            'section': section
        }

        return render(request, 'dashboard/teacher/section_view.html', context=data)


@login_required
def attendance_list(request, pk, section):
    user_id = pk

    user_model = get_user_model()
    user = user_model.objects.get(pk=user_id)

    if user.has_perm('accounts.set_teacher_status'):

        data = {
            "user": user,
            "section": section,
            "attendances": user.attendance_records.filter(section=section)
        }

        return render(request, 'dashboard/teacher/attendance_list.html', context=data)


@login_required
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
            'user': user,
            'attendance': attendance_record
        }

        return render(request, 'dashboard/teacher/attendance_view.html', context=data)
