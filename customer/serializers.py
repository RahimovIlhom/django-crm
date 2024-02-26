from rest_framework import serializers

from attendance.serializers import AttendanceSerializer
from course.models import Course
from course.serializers import CourseSerializer
from group.serializers import GroupListSerializer
from payment.serializers import PaymentSerializer
from .models import Mentor, Student


class MentorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    group_count = serializers.SerializerMethodField('get_group_count')
    course_info = serializers.SerializerMethodField('get_course')

    class Meta:
        model = Mentor
        fields = ['id', 'fullname', 'phone_number', 'photo', 'location', 'course', 'course_info', 'group_count']

    def get_group_count(self, obj):
        return obj.groups.count()

    def get_course(self, obj):
        return CourseSerializer(obj.course).data


class MentorRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    group_count = serializers.SerializerMethodField('get_group_count')
    groups = serializers.SerializerMethodField('get_groups')
    course_info = serializers.SerializerMethodField('get_course')

    class Meta:
        model = Mentor
        fields = ['id', 'fullname', 'phone_number', 'photo', 'location', 'course', 'course_info', 'group_count',
                  'groups']

    def get_group_count(self, obj):
        return obj.groups.count()

    def get_course(self, obj):
        return CourseSerializer(obj.course).data

    def get_groups(self, obj):
        groups = obj.groups.all()
        return GroupListSerializer(instance=groups, many=True).data


class StudentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    balance = serializers.DecimalField(max_digits=11, decimal_places=2, default=0, read_only=True, required=False)
    status = serializers.CharField(max_length=20, read_only=True, required=False)
    course_info = serializers.SerializerMethodField('get_course')
    group_info = serializers.SerializerMethodField('get_group')

    class Meta:
        model = Student
        fields = ['id', 'fullname', 'phone_number', 'parents', 'course', 'course_info', 'group', 'group_info',
                  'balance', 'created_time', 'update_time', 'status']

    def get_course(self, obj):
        return CourseSerializer(obj.course).data

    def get_group(self, obj):
        return GroupListSerializer(obj.group).data

    def create(self, validated_data):
        group = validated_data.get('group', None)
        student = Student.objects.create(**validated_data)
        if group:
            student.status = group.status
            student.save()
        return student

    def update(self, instance, validated_data):
        group = validated_data.get('group', None)
        if group:
            instance.group = group
            instance.status = group.status
            instance.save()
        return instance


class StudentRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    balance = serializers.DecimalField(max_digits=11, decimal_places=2, default=0, read_only=True, required=False)
    status = serializers.CharField(max_length=20, read_only=True, required=False)
    course_info = serializers.SerializerMethodField('get_course')
    group_info = serializers.SerializerMethodField('get_group')
    attendances = serializers.SerializerMethodField('get_attendances')
    payments = serializers.SerializerMethodField('get_payments')

    class Meta:
        model = Student
        fields = ['id', 'fullname', 'phone_number', 'parents', 'course', 'course_info', 'group', 'group_info',
                  'balance', 'created_time', 'update_time', 'status', 'attendances', 'payments']

    def get_course(self, obj):
        return CourseSerializer(obj.course).data

    def get_group(self, obj):
        return GroupListSerializer(obj.group).data

    def get_attendances(self, obj):
        attendances = obj.attendances.all()
        return AttendanceSerializer(attendances, many=True).data

    def get_payments(self, obj):
        payments = obj.payments.all()
        return PaymentSerializer(payments, many=True).data
