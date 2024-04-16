from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from notifications.signals import notify
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.end_session_serializer import EndSessionSerializer
from ..authentication import authenticate_each_models
from accounts.models.tag import Tag
from rooms.models.scanner import Scanner
from attendances.models.attendance import Attendance


@method_decorator(csrf_exempt, name='dispatch')
class EndSessionApiView(APIView):
    def patch(self, request):
        data = {
            'purpose': request.data.get('purpose'),
            'scanner_id': request.date.get('scanner_id'),
            'attendance_id': request.data.get('attendance_id'),
            'tag_id': request.data.get('tag_id'),
            'time_at': request.data.get('time_at')
        }

        serializer = EndSessionSerializer(data=data)

        # validate data
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        tag_id = serializer.validated_data.get('tag_id')
        scanner_id = serializer.validated_data.get('scanner_id')
        attendance_id = serializer.validated_data.get('attendance_id')

        # authenticate
        all_authenticated, results = authenticate_each_models(
            (Tag, tag_id),
            (Attendance, attendance_id),
            (Scanner, scanner_id)
        )

        if not all_authenticated:
            return Response(
                data={
                    "Error": f'{results}'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        tag, attendance, scanner = results

        user = tag.user
        room = scanner.designated_room

        time_at = serializer.validated_data.get('time_at')
        purpose = serializer.validated_data.get('purpose')

        if tag.is_compromised:
            notify.send(
                None,
                recipient=user,
                verb=f"Compromised Tag is used at {room.name} at {time_at}"
            )

        # find the attendance and set end_at
        if user.has_perm('accounts.set_teacher_status') and user:
            attendance.end_at = time_at
            attendance.save()

            # set all the attendees end_at
            attendance.attendee_records.update(end_at=time_at)

            return Response(
                data={
                    'Message' f'Ended session at room {room.name}'
                },
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                data={
                    'Error': f'User {user.last_name} has no permission for {purpose}',
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
