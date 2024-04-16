from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers.attendances import CreateAttendanceSerializer, AttendAndEndAttendanceSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import Http404
from notifications.signals import notify
from rooms.models.scanner import Scanner
from attendances.models.attendance import Attendance
from attendances.models.attendee import Attendee
from schedules.utils import get_nearest_schedule
from accounts.models.tag import Tag


@api_view(['POST'])
def create_attendance(request):
    """
        Create an attendance to a room
    """
    serializer = CreateAttendanceSerializer(data=request.data)

    if serializer.is_valid():

        if not serializer.validated_data['purpose'] == "CREATE_SESSION":
            return Response(
                data={"Message": "Purpose is wrong"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        # authenticate data
        user_model = get_user_model()

        try:
            user = get_object_or_404(user_model, tags__pk=serializer.validated_data['tag_id'])
        except Http404 as e:
            return Response(
                data={"Message": "User not found", "Error": e},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            tag = get_object_or_404(Tag, pk=serializer.validated_data['tag_id'])
        except Http404 as e:
            return Response(
                data={"Message": "Tag not found", "Error": e},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            scanner = get_object_or_404(Scanner, pk=serializer.validated_data['device_id'])
        except Http404 as e:
            return Response(
                data={"Message": "Room not found", "Error": e},
                status=status.HTTP_404_NOT_FOUND
            )

        room = scanner.designated_room

        # send notif of compromised tag is used
        if tag.is_compromised:
            notify.send(
                sender=None,
                recipient=user,
                verb=f"Compromised tag of {user.last_name} is used at {room.name}"
            )

        if room.is_available:
            # find the nearest schedule
            time_in = serializer.validated_data['time_in']
            schedule_unit = get_nearest_schedule(user, time_in)

            # create attendance
            attendance = Attendance.objects.create(
                room=room,
                teacher=user,
                section=schedule_unit.section,
                subject=schedule_unit.subject
            )

            room.is_available = False
            room.save()

            return Response(
                data={
                    "Message": "Attendance Created",
                    "attendance_id": attendance.pk
                },
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                data={"Message": "Room is occupied"},
                status=status.HTTP_409_CONFLICT
            )

    else:
        return Response(
            data={"Message": "Invalid Data", "Error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def attend_attendance(request):
    serializer = AttendAndEndAttendanceSerializer(data=request.data)

    if serializer.is_valid():

        if not serializer.validated_data['purpose'] == "ATTEND_SESSION":
            return Response(
                data={"Message": "Purpose is wrong"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        # authenticate data
        user_model = get_user_model()

        try:
            user = get_object_or_404(user_model, tags__pk=serializer.validated_data['tag_id'])
        except Http404 as e:
            return Response(
                data={"Message": "Tag not found", "Error": e},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            tag = get_object_or_404(Tag, pk=serializer.validated_data['tag_id'])
        except Http404 as e:
            return Response(
                data={"Message": "Tag not found", "Error": e},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            scanner = get_object_or_404(Scanner, pk=serializer.validated_data['device_id'])
        except Http404 as e:
            return Response(
                data={"Message": "Room not found", "Error": e},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            attendance = get_object_or_404(Attendance, pk=serializer.validated_data['attendance_id'])
        except Http404 as e:
            return Response(
                data={"Message": "Attendance not found", "Error": e},
                status=status.HTTP_404_NOT_FOUND
            )

        room = scanner.designated_room

        # send notif of compromised tag is used
        if tag.is_compromised:
            notify.send(
                sender=None,
                recipient=attendance.teacher,
                verb=f"Compromised tag of {user.last_name} is used at {room.name}"
            )

        if attendance.on_going:
            # if still available
            Attendee.objects.create(
                attendance=attendance,
                user=user,
                starting_at=serializer.validated_data['time_in']
            )

            return Response(
                data={"Message": "Attended"},
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                data={"Message": "Attendance is closed"},
                status=status.HTTP_409_CONFLICT
            )

    else:
        return Response(
            data={"Message": "Invalid Data", "Error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PATCH'])
def end_attendance(request):
    serializer = AttendAndEndAttendanceSerializer(data=request.data)

    if serializer.is_valid():

        if not serializer.validated_data['purpose'] == "END_SESSION":
            return Response(
                data={"Message": "Purpose is wrong"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        # authenticate data
        user_model = get_user_model()

        try:
            user = get_object_or_404(user_model, tags__pk=serializer.validated_data['tag_id'])
        except Http404 as e:
            return Response(
                data={"Message": "Tag not found", "Error": e},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            tag = get_object_or_404(Tag, pk=serializer.validated_data['tag_id'])
        except Http404 as e:
            return Response(
                data={"Message": "Tag not found", "Error": e},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            scanner = get_object_or_404(Scanner, pk=serializer.validated_data['device_id'])
        except Http404 as e:
            return Response(
                data={"Message": "Room not found", "Error": e},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            attendance = get_object_or_404(Attendance, pk=serializer.validated_data['attendance_id'])
        except Http404 as e:
            return Response(
                data={"Message": "Attendance not found", "Error": e},
                status=status.HTTP_404_NOT_FOUND
            )

        room = scanner.designated_room

        # send notif of compromised tag is used
        if tag.is_compromised:
            notify.send(
                sender=None,
                recipient=attendance.teacher,
                verb=f"Compromised tag of {user.last_name} is used at {room.name}"
            )

        # close the attendance
        attendance.on_going = False
        attendance.end_at = serializer.validated_data['time_in']
        attendance.save()

        Attendee.objects.filter(
            attendance__pk=attendance.pk
        ).update(end_at=serializer.validated_data['time_in'])

        # update the availability of the room
        room.is_available = True
        room.save()

        return Response(
            data={"Message": "Attendance Closed"},
            status=status.HTTP_200_OK
        )

    else:
        return Response(
            data={"Message": "Invalid Data", "Error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
