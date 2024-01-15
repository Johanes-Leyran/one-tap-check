from rest_framework import serializers
from rooms.models import Room
from attendances.models import Attendance


class RoomAvailabilitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Room
        fields = ['uuid', 'is_available']
  
  
class TapInSerializerTeacher(serializers.ModelSerializer):
    room_uuid = serializers.UUIDField()
    user_uuid = serializers.UUIDField()
    
    class Meta:
        model = Attendance
        fields = ['room_uuid', 'user_uuid']
    
    
class TapInSerializerStudent(serializers.ModelSerializer):
    user_uuid = serializers.UUIDField()
    attendance_id = serializers.UUIDField()
    
    class Meta:
        model = Attendance
        fields = ['user_uuid', 'attendance_id']