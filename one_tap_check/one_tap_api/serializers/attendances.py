from rest_framework import serializers
from utils.cuid import CUID_TAG, CUID_SCANNER, CUID_ATTENDANCE

LIST_PURPOSE = ['CREATE_SESSION', 'ATTEND_SESSION', 'END_SESSION']


class AttendanceSerializer(serializers.Serializer):
    pass


class CreateAttendanceSerializer(serializers.Serializer):
    purpose = serializers.CharField()
    device_id = serializers.CharField()
    tag_id = serializers.CharField()
    # From the arduino the format of the time in ISO 8601
    time_in = serializers.DateTimeField()

    def validate(self, attrs):
        errors = {}
        purpose = attrs.get('purpose')

        if purpose not in LIST_PURPOSE:
            errors['purpose'] = 'Purpose is invalid'

        device_id = attrs.get('device_id')
        tag_id = attrs.get('tag_id')

        if not CUID_SCANNER.validate(device_id):
            errors['device_id'] = 'Device ID is not valid'

        if not CUID_TAG.validate(tag_id):
            errors['tag_id'] = "Tag ID is not valid"

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class AttendAndEndAttendanceSerializer(serializers.Serializer):
    purpose = serializers.CharField()
    device_id = serializers.CharField()
    tag_id = serializers.CharField()
    attendance_id = serializers.CharField()
    time_in = serializers.DateTimeField()

    def validate(self, attrs):
        errors = {}
        purpose = attrs.get('purpose')

        if purpose not in LIST_PURPOSE:
            errors['purpose'] = 'Purpose is invalid'

        device_id = attrs.get('device_id')
        tag_id = attrs.get('tag_id')
        attendance_id = attrs.get('attendance_id')

        if not CUID_SCANNER.validate(device_id):
            errors['device_id'] = 'Device ID is not valid'

        if not CUID_TAG.validate(tag_id):
            errors['tag_id'] = "Tag ID is not valid"

        if not CUID_ATTENDANCE.validate(attendance_id):
            errors['tag_id'] = "Tag ID is not valid"

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
