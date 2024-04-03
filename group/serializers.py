from django.utils.module_loading import import_string
from rest_framework import serializers

from course.serializers import CourseSerializer
from group.models import Group


class GroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    continuity = serializers.IntegerField(default=6)
    created_time = serializers.DateTimeField(read_only=True)
    started_time = serializers.DateTimeField(read_only=True)
    finished_time = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(max_length=20, read_only=True)
    students_count = serializers.SerializerMethodField('get_students_count')

    class Meta:
        model = Group
        fields = ['id', 'title', 'course', 'continuity', 'mentor', 'lesson_start_time', 'lesson_end_time', 'image',
                  'created_time', 'started_time', 'finished_time', 'status', 'study_day', 'students_count']

    def get_students_count(self, obj):
        return obj.students.count()


class GroupListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    continuity = serializers.IntegerField(default=6)
    created_time = serializers.DateTimeField(read_only=True)
    started_time = serializers.DateTimeField(read_only=True)
    finished_time = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(max_length=20, read_only=True)
    course_info = serializers.SerializerMethodField('get_course_info')
    mentor_info = serializers.SerializerMethodField('get_mentor_info')
    students_count = serializers.SerializerMethodField('get_students_count')

    class Meta:
        model = Group
        fields = ['id', 'title', 'course', 'continuity', 'course_info', 'mentor', 'mentor_info', 'lesson_start_time', 'lesson_end_time', 'image', 'created_time',
                  'started_time', 'finished_time', 'status', 'study_day', 'students_count']

    def get_course_info(self, obj) -> dict:
        return CourseSerializer(obj.course).data

    def get_mentor_info(self, obj) -> dict:
        mentor_serializer_class = 'customer.serializers.MentorSerializers'
        MentorSerializers = import_string(mentor_serializer_class)
        return MentorSerializers(obj.mentor).data

    def get_students_count(self, obj):
        return obj.students.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['course_info'] = self.get_course_info(instance)
        data['mentor_info'] = self.get_mentor_info(instance)
        return data


class GroupRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    continuity = serializers.IntegerField(default=6)
    created_time = serializers.DateTimeField(read_only=True)
    started_time = serializers.DateTimeField(read_only=True)
    finished_time = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(max_length=20, read_only=True)
    course_info = serializers.SerializerMethodField('get_course_info')
    mentor_info = serializers.SerializerMethodField('get_mentor_info')
    students = serializers.SerializerMethodField('get_students')
    students_count = serializers.SerializerMethodField('get_students_count')

    class Meta:
        model = Group
        fields = ['id', 'title', 'course', 'continuity', 'course_info', 'mentor', 'mentor_info', 'lesson_start_time', 'lesson_end_time', 'image', 'created_time',
                  'started_time', 'finished_time', 'status', 'study_day', 'students', 'students_count']

    def get_course_info(self, obj) -> dict:
        return CourseSerializer(obj.course).data

    def get_mentor_info(self, obj) -> dict:
        from customer.serializers import MentorSerializers
        return MentorSerializers(obj.mentor).data

    def get_students(self, obj) -> list:
        from customer.serializers import StudentSerializers
        month = self.context.get('month')
        year = self.context.get('year')
        serialized_students = StudentSerializers(obj.students.filter(status=obj.status), many=True, context={'year': year, 'month': month}).data
        return serialized_students

    def get_students_count(self, obj):
        return obj.students.count()


class StudentGroupAssignmentSerializer(serializers.Serializer):
    student_id = serializers.IntegerField(
        required=True,
        write_only=True,
    )
    group_id = serializers.IntegerField(
        required=True,
        write_only=True,
    )

    def to_representation(self, instance):
        return {
            'student_id': instance.get('student_id', ''),
            'group_id': instance.get('group_id', ''),
        }


class StartCompletedGroupSerializer(serializers.Serializer):
    group_id = serializers.IntegerField(
        required=True,
        write_only=True,
    )

    def to_representation(self, instance):
        return {
            'group_id': instance.get('group_id', ''),
        }


class AttachTeacherSerializer(serializers.Serializer):
    group_id = serializers.IntegerField(
        required=True,
        write_only=True,
    )
    mentor_id = serializers.IntegerField(
        required=True,
        write_only=True,
    )

    def to_representation(self, instance):
        return {
            'mentor_id': instance.get('mentor_id', ''),
            'group_id': instance.get('group_id', ''),
        }


class ReleaseTeacherSerializer(serializers.Serializer):
    group_id = serializers.IntegerField(
        required=True,
        write_only=True,
    )

    def to_representation(self, instance):
        return {
            'group_id': instance.get('group_id', ''),
        }


class AttendanceGroupSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    students_attendance = serializers.DictField(child=serializers.BooleanField())

    def validate(self, data):
        if 'group_id' not in data:
            raise serializers.ValidationError("group_id is required")

        if not isinstance(data.get('students_attendance', {}), dict):
            raise serializers.ValidationError("students_attendance should be a dictionary")

        return data
