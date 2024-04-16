from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ..serializers.create_session_serializer import CreateSessionSerializer
from accounts.models.tag import Tag
from rooms.models.scanner import Scanner
from attendances.models.attendance import Attendance
from ..authentication import authenticate_each_models
from notifications.signals import notify
# Todo: make them async


@method_decorator(csrf_exempt, name='dispatch')
class CreateSessionApiView(APIView):
    def post(self, request) -> Response:
        data = {
            'purpose': request.data.get('purpose'),
            'scanner_id': request.date.get('scanner_id'),
            'tag_id': request.data.get('tag_id'),
            'time_at': request.data.get('time_at')
        }

        serializer = CreateSessionSerializer(data=data)

        # validate the data from arduino
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        tag_id = serializer.validated_data.get('tag_id')
        scanner_id = serializer.validated_data.get('device_id')

        all_authenticated, results = authenticate_each_models(
            (Tag, tag_id),
            (Scanner, scanner_id)
        )

        if not all_authenticated:
            return Response(
                data={
                    "Error": f'{results}'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        tag, scanner = results

        # get the user of the tag and the room of the scanner
        user = tag.user
        room = scanner.designated_room

        attended_at = serializer.validated_data.get('time_at')

        if tag.is_compromised:
            notify.send(
                None,
                recipient=user,
                verb=f"Compromised Tag is used at {room.name} at {attended_at}"
            )

        # check if the room is available
        if not room.is_available:
            return Response(
                data={
                    "Error": f"Room {room.name} is occupied"
                },
                status=status.HTTP_409_CONFLICT
            )

        purpose = serializer.validated_data.get('purpose')

        # check if the user has permission to create a session
        if user.has_perm('accounts.set_teacher_status') and user and room:
            attendance = Attendance.object.create(
                room=room,
                teacher=user,
                starting_at=attended_at
            )

            # update the availability of that room
            room.is_available = False
            room.save()

            return Response(
                data={
                    'Message': f'Created a session on room {room.name}',
                    'Attendance ID': attendance.pk,
                    'Teacher Name': user.last_name
                },
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                data={
                    'Error': f'{user.last_name} has no permission for {purpose}'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
