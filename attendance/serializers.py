from rest_framework import serializers

from attendance.models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = '__all__'


class AttendanceListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    student_info = serializers.SerializerMethodField('get_student_info')
    date = serializers.DateField(read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_info', 'attended', 'date']

    def get_student_info(self, obj) -> dict:
        from customer.serializers import StudentSerializers
        return StudentSerializers(obj.student).data


class AttendanceRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    student_info = serializers.SerializerMethodField('get_student_info')
    date = serializers.DateField(read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_info', 'attended', 'date']

    def get_student_info(self, obj) -> dict:
        from customer.serializers import StudentSerializer
        return StudentSerializer(obj.student).data
