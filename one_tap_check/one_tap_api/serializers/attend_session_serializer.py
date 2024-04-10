from rest_framework import serializers
from utils.cuid import CUID_SCANNER, CUID_TAG, CUID_ATTENDANCE


class AttendSessionSerializer(serializers.Serializer):
    purpose = serializers.CharField()
    device_id = serializers.CharField()
    tag_id = serializers.CharField()
    attendance_id = serializers.CharField()
    time = serializers.DateTimeField()

    def validate_purpose(self, value) -> serializers.ValidationError | str:
        if value != "ATTEND_SESSION":
            return serializers.ValidationError("Purpose is not aligned")

        return value

    def validate_device_id(self, value) -> serializers.ValidationError | str:
        if not CUID_SCANNER.validate(value):
            return serializers.ValidationError("Device ID is invalid")

        return value

    def validate_tag_id(self, value) -> serializers.ValidationError | str:
        if not CUID_TAG.validate(value):
            return serializers.ValidationError("Tag ID is invalid")

        return value

    def validate_attendance_id(self, value) -> serializers.ValidationError | str:
        if not CUID_ATTENDANCE.validate(value):
            return serializers.ValidationError("Tag ID is invalid")

        return value
