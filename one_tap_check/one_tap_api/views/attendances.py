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

        if serializer.validated_data['purpose'] != "CREATE_SESSION":
            return Response(
                data={"Message": "Purpose is wrong"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        # authenticate tag
        try:
            user = get_object_or_404(get_user_model(), tags__pk=serializer.validated_data['tag_id'])
        except Http404 as e:
            return Response(
                data={"Message": "User not found", "Error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

        if not user.has_perm("accounts.set_teacher_status"):
            return Response(
                data={"Message": f"{user.last_name} no auth"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            tag = get_object_or_404(Tag, pk=serializer.validated_data['tag_id'])
        except Http404 as e:
            return Response(
                data={"Message": "Tag not found", "Error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

        # authenticate the scanner
        try:
            scanner = get_object_or_404(Scanner, pk=serializer.validated_data['device_id'])
        except Http404 as e:
            return Response(
                data={"Message": "Scanner not found", "Error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

        # check if they are none
        if not tag:
            return Response(
                data={"Message": "Tag is none"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not scanner:
            return Response(
                data={"Message": "Scanner is none"},
                status=status.HTTP_404_NOT_FOUND
            )

        room = scanner.designated_room

        if not room:
            return Response(
                data={"Message": "Scanner has no room"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # # send notif of compromised tag is used
        # if user and tag.is_compromised:
        #     notify.send(
        #         sender=None,
        #         recipient=user,
        #         verb=f"Compromised tag of {user.last_name} is used at {room.name}"
        #     )
        # else:
        #     notify.send(
        #         sender=None,
        #         recipient=user,
        #         verb=f"Compromised tag is used at {room.name}"
        #     )

        if room.is_available:
            time_in = serializer.validated_data['time_in']

            try:
                attendance = Attendance.objects.create(
                    room=room,
                    teacher=user,
                    starting_at=time_in
                )

            # if creating attendance fail
            except Exception as e:
                return Response(
                    data={
                        "Message": f"{type(e)}",
                        "Error": f"When creating attendance exception raised: {str(e)}"
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            room.is_available = False
            room.save()

            return Response(
                data={
                    "Message": "Attendance Created",
                    "attendance_id": attendance.pk,
                    "teacher_name": user.last_name
                },
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                data={"Message": "Room occupied"},
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

        if serializer.validated_data['purpose'] != "ATTEND_SESSION":
            return Response(
                data={"Message": "Purpose is wrong"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        try:
            user = get_object_or_404(get_user_model(), tags__pk=serializer.validated_data['tag_id'])
        except Http404 as e:
            return Response(
                data={"Message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not user.has_perm("accounts.set_student_status"):
            return Response(
                data={"Message": f"{user.last_name} no auth"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            tag = get_object_or_404(Tag, pk=serializer.validated_data['tag_id'])
        except Http404 as e:
            return Response(
                data={"Message": "Tag not found", "Error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            scanner = get_object_or_404(Scanner, pk=serializer.validated_data['device_id'])
        except Http404 as e:
            return Response(
                data={"Message": "Scanner not found", "Error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            attendance = get_object_or_404(Attendance, pk=serializer.validated_data['attendance_id'])
        except Http404 as e:
            return Response(
                data={"Message": "Attendance not found", "Error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

        room = scanner.designated_room

        if not room:
            return Response(
                data={"Message": "Scanner has no room"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # if tag has no associated user
        if not user:
            return Response(
                data={"Message": "Tag has no user"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # send notif of compromised tag is used
        # if user and tag.is_compromised:
        #     notify.send(
        #         sender=None,
        #         recipient=user,
        #         verb=f"Compromised tag of {user.last_name} is used at {room.name}"
        #     )
        # else:
        #     notify.send(
        #         sender=None,
        #         recipient=user,
        #         verb=f"Compromised tag is used at {room.name}"
        #     )

        # if tag has no associated user
        if not user:
            return Response(
                data={"Message": "Tag has no user"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if attendance.on_going:

            # if still available
            Attendee.objects.create(
                attendance=attendance,
                user=user,
                starting_at=serializer.validated_data['time_in']
            )

            return Response(
                data={"Message": "Attended", "student_name": user.last_name},
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                data={"Message": "Attendance over"},
                status=status.HTTP_409_CONFLICT
            )

    else:
        return Response(
            data={"Message": "Invalid Data", "Error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def end_attendance(request):
    serializer = AttendAndEndAttendanceSerializer(data=request.data)

    if serializer.is_valid():

        if serializer.validated_data['purpose'] != "END_SESSION":
            return Response(
                data={"Message": "Purpose is wrong"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        try:
            user = get_object_or_404(get_user_model(), tags__pk=serializer.validated_data['tag_id'])
        except Http404 as e:
            return Response(
                data={"Message": "User not found", "Error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

        if not user.has_perm("accounts.set_teacher_status"):
            return Response(
                data={"Message": f"{user.last_name} no auth"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # authenticate data
        try:
            tag = get_object_or_404(Tag, pk=serializer.validated_data['tag_id'])
        except Http404 as e:
            return Response(
                data={"Message": "Tag not found", "Error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            scanner = get_object_or_404(Scanner, pk=serializer.validated_data['device_id'])
        except Http404 as e:
            return Response(
                data={"Message": "Scanner not found", "Error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            attendance = get_object_or_404(Attendance, pk=serializer.validated_data['attendance_id'])
        except Http404 as e:
            return Response(
                data={"Message": "Attendance not found", "Error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

        room = scanner.designated_room

        if not room:
            return Response(
                data={"Message": "Scanner has no room"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # if tag has no associated user
        if not user:
            return Response(
                data={"Message": "Tag has no user"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # send notif of compromised tag is used
        # if user and tag.is_compromised:
        #     notify.send(
        #         sender=None,
        #         recipient=user,
        #         verb=f"Compromised tag of {user.last_name} is used at {room.name}"
        #     )
        # else:
        #     notify.send(
        #         sender=None,
        #         recipient=user,
        #         verb=f"Compromised tag is used at {room.name}"
        #     )

        # if tag has no associated user
        if not user:
            return Response(
                data={"Message": "Tag has no user"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # close the attendance
        attendance.on_going = False
        attendance.end_at = serializer.validated_data['time_in']
        attendance.save()

        # get all the attendee that has not tap out but tapped in
        # they will be marked as absent
        Attendee.objects.filter(
            attendance__pk=attendance.pk,
            end_at__isnull=True
        ).update(status="Absent")

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
