from rest_framework.response import Response
from rest_framework import views
from rest_framework import status
from .serializer import TapInSerializerStudent, TapInSerializerTeacher
from attendances.models import Attendance, Attendee
from rooms.models import Room
from django.contrib.auth import get_user_model
from django import http


class RoomTapInView(views.APIView):
    def get_object(self, serializer, model, field):
        uuid = serializer.validated_data[field]
        
        try:
            return model.objects.get(uuid=uuid)
        except model.DoesNotExist:
            raise http.Http404(f"not found in {model}")
    
    def post(self, request):
        serializer = TapInSerializerTeacher(data=request.data)
        
        if not serializer.is_valid():
            return Response({'error': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        
        # teacher = self.get_object(serializer, get_user_model, 'user_uuid')
        # room = self.get_object(serializer, Room, 'room_uuid')
        
        teacher_uuid = serializer.validated_data['user_uuid']
        room_uuid = serializer.validated_data['room_uuid']
        
        try:
            teacher = get_user_model().objects.get(uuid=teacher_uuid)
            room = Room.objects.get(uuid=room_uuid)
        except:
            raise http.Http404(f"not found")
            
        
        if not teacher.is_teacher:
            return Response({'error': 'user has no permission'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not room.is_available:
            return Response({'error': 'room is not available'}, status=status.HTTP_403_FORBIDDEN)
            
        
        attendance = Attendance.objects.create(room=room, teacher=teacher)
        attendance.save()
        room.is_available = False
        room.save()
        
        return Response(
            {'success': 'attendance created', 'attendance_id': attendance.pk},
            status=status.HTTP_201_CREATED
        )    
            
    def patch(self, request):
        serializer = TapInSerializerStudent(data=request.data)
        
        if not serializer.is_valid():
            return Response({'error': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        
        student_uuid = serializer.validated_data['user_uuid']
        attendance_id = serializer.validated_data['attendance_id']
            
        try:
            student = get_user_model().objects.get(uuid=student_uuid)
            attendance = Room.objects.get(id=attendance_id)
        except Attendance.DoesNotExist:
            raise http.Http404(f"attendance not found")
        except get_user_model().DoesNotExist:
            raise http.Http404(f"user not found")
        
        attendee = Attendee.objects.create(attendance=attendance, user=student)
        attendee.save()
        
        return Response({'succes': 'attendee created'}, status=status.HTTP_201_CREATED)
    