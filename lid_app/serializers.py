from rest_framework import serializers

from course.serializers import CourseSerializer
from group.serializers import GroupSerializer
from lid_app.models import Lid, Contact


class LidSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    balance = serializers.DecimalField(max_digits=11, decimal_places=2, default=0, read_only=True, required=False)
    status = serializers.CharField(max_length=20, read_only=True, required=False)
    course_info = serializers.SerializerMethodField('get_course')
    group_info = serializers.SerializerMethodField('get_group')

    class Meta:
        model = Lid
        fields = ['id', 'fullname', 'phone_number', 'parents', 'coming', 'course', 'school', 'course_info', 'group', 'group_info',
                  'balance', 'created_time', 'update_time', 'status']

    def get_course(self, obj) -> dict:
        return CourseSerializer(obj.course).data

    def get_group(self, obj) -> dict:
        return GroupSerializer(obj.group).data


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'
