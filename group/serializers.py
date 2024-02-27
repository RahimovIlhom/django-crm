from rest_framework import serializers

from course.serializers import CourseSerializer
from group.models import Group


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class GroupListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_time = serializers.DateTimeField(read_only=True)
    started_time = serializers.DateTimeField(read_only=True)
    finished_time = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(max_length=20, read_only=True)
    course_info = serializers.SerializerMethodField('get_course_info')
    mentor_info = serializers.SerializerMethodField('get_mentor_info')
    students_count = serializers.SerializerMethodField('get_students_count')

    class Meta:
        model = Group
        fields = ['id', 'title', 'course', 'course_info', 'mentor', 'mentor_info', 'image', 'created_time', 'started_time',
                  'finished_time', 'status', 'students_count']

    def get_course_info(self, obj):
        return CourseSerializer(obj.course).data

    def get_mentor_info(self, obj):
        from customer.serializers import MentorSerializers
        return MentorSerializers(obj.mentor).data

    def get_students_count(self, obj):
        return obj.students.count()


class GroupRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
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
        fields = ['id', 'title', 'course', 'course_info', 'mentor', 'mentor_info', 'image', 'created_time', 'started_time',
                  'finished_time', 'status', 'students', 'students_count']

    def get_course_info(self, obj):
        return CourseSerializer(obj.course).data

    def get_mentor_info(self, obj):
        from customer.serializers import MentorSerializers
        return MentorSerializers(obj.mentor).data

    def get_students(self, obj):
        from customer.serializers import StudentSerializers
        return StudentSerializers(obj.students.all(), many=True).data

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
