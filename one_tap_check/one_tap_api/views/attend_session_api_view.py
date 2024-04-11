from rest_framework.response import Response
from ..serializers.attend_session_serializer import AttendSessionSerializer
from ..authentication import authenticate_each_models
from rest_framework.views import APIView
from rest_framework import status
from accounts.models.tag import Tag
from rooms.models.scanner import Scanner
from attendance.models.attendance import Attendance
from attendance.models.attendee import Attendee


class AttendSessionApiView(APIView):
    def post(self, request):
        data = {
            'purpose': request.data.get('purpose'),
            'scanner_id': request.date.get('scanner_id'),
            'tag_id': request.data.get('tag_id'),
            'attendance': request.data.get('attendance_id'),
            'time_at': request.data.get('time_at')
        }

        serializer = AttendSessionSerializer(data=data)

        # validate the data
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        tag_id = serializer.validated_data.get('tag_id')
        scanner_id = serializer.validated_data.get('scanner_id')
        attendance_id = serializer.validated_data.get('attendance_id')
        time_at = serializer.validated_data.get('time_at')
        purpose = serializer.validated_data.get('purpose')

        # authenticate
        all_authenticated, results = authenticate_each_models(
            (Tag, tag_id),
            (Scanner, scanner_id),
            (Attendance, attendance_id)
        )

        if not all_authenticated:
            return Response(
                data={
                    "Error": f'{results}',
                },
                status=status.HTTP_404_NOT_FOUND
            )

        tag, scanner, attendance = results

        user = tag.user
        room = scanner.designated_room

        # check permissions
        # Todo: be more precise on the error
        if user.has_perm("accounts.set_student_status") and user and room:
            # Todo: check if the attendance is still on going or not

            Attendee.objects.create(
                user=user,
                attendance=attendance,
                start_at=time_at
            )

            return Response(
                data={
                    'Message': f'Created a Attendee for {attendance.starting_at} at room {room.name}'
                },
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                data={
                    "Error": f'User {user.last_name} has no permission for {purpose}'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
