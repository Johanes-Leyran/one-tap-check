from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ..serializers.create_session_serializer import CreateSessionSerializer
from accounts.models.tag import Tag
from rooms.models.scanner import Scanner
from attendance.models.attendance import Attendance
from ..authentication import authenticate_model


class CreateSessionApiView(APIView):
    def post(self, requests):
        data = {
            'purpose': requests.data.get('purpose'),
            'device_id': requests.date.get('device_id'),
            'tag_id': requests.data.get('tag_id'),
            'time_at': requests.data.get('time')
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

        # authenticate the tag and the device id
        try:
            tag = authenticate_model(Tag, tag_id)
            scanner = authenticate_model(Scanner, scanner_id)

        except Http404 as e:
            return Response(
                {'Error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

        # get the user of the tag and the room of the scanner
        user = tag.user
        room = scanner.designated_room

        attended_at = serializer.validated_data.get('time_at')

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

        else:
            return Response(
                data={
                    'Error': f'User {user.last_name} has no permission to create a session'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            data={
                'Message': f'Created a session on room {room.name}',
                'Attendance ID': attendance.pk
            },
            status=status.HTTP_201_CREATED
        )
