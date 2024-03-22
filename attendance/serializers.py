from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from attendance.models import Attendance
from customer.models import Student


class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    attended = serializers.BooleanField(required=False, default=False)
    date = serializers.DateField(required=False)

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'attended', 'date']

    def create(self, validated_data):
        student = validated_data.get('student')
        attended = validated_data.get('attended', False)
        date = validated_data.get('date', timezone.now().date())

        if student.status == 'continues':
            attendance, created = Attendance.objects.get_or_create(student=student, date=date)
            if created is False:
                attendance.attended = attended
                attendance.save()
                return attendance
            else:
                attendance.attended = attended
                attendance.save()
                return attendance
        else:
            data = {
                'success': False,
                'message': "Studentni yo'qlama qilish uchun guruh start olgan bo'lishi kerak!"
            }
            raise ValidationError(data)


class AttendanceListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    student_info = serializers.SerializerMethodField('get_student_info')
    date = serializers.DateField(read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_info', 'attended', 'date']

    def get_student_info(self, obj) -> dict:
        from customer.serializers import StudentSerializer
        return StudentSerializer(obj.student).data


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
