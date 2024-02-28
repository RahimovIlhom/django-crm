from django.utils import timezone
from django.db.models import Q
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.models import Attendance
from customer.models import Student, Mentor
from .models import Group
from .serializers import GroupListSerializer, GroupSerializer, GroupRetrieveSerializer, \
    StudentGroupAssignmentSerializer, StartCompletedGroupSerializer, AttachTeacherSerializer, ReleaseTeacherSerializer, \
    AttendanceGroupSerializer


class GroupListAPIView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(status='no_started') | Q(status='continues'))
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    def get(self, request, *args, **kwargs):
        """
        Filter mentors by course_id. Example: .../api/groups/all/?course_id={course_id}
        """
        return super().list(request, *args, **kwargs)


class GroupCreateAPIView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupListSerializer


class GroupRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupRetrieveSerializer


class GroupUpdateAPIView(generics.UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupListSerializer


class GroupDeleteAPIView(generics.DestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'deleted'
        instance.save()
        students = instance.students.all()
        for student in students:
            student.status = 'deleted'
            student.save()
        data = {'success': True, 'message': "The group has been deleted and its readers have been added to the "
                                            "deleted list!"}
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class AddStudentToGroup(generics.CreateAPIView):
    serializer_class = StudentGroupAssignmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student_id = serializer.validated_data.get('student_id')
        group_id = serializer.validated_data.get('group_id')

        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Response({'success': False, "message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({'success': False, "message": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        if student.group == group:
            return Response({'success': False, 'message': 'The student has already joined the specified group'},
                            status=status.HTTP_400_BAD_REQUEST)

        student.group = group
        student.status = group.status
        student.save()

        return Response({"success": True, 'message': f"Student {student.fullname} added to group {group.title}"},
                        status=status.HTTP_201_CREATED)


class RemoveStudentFromGroup(generics.CreateAPIView):
    serializer_class = StudentGroupAssignmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student_id = serializer.validated_data.get('student_id')
        group_id = serializer.validated_data.get('group_id')

        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Response({'success': False, "message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({'success': False, "message": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        if student.group != group:
            return Response({'success': False, 'message': 'Student is not assigned to the specified group'},
                            status=status.HTTP_400_BAD_REQUEST)

        student.group = None
        student.status = 'no_started'
        student.save()

        return Response({'success': True, 'message': f'Student {student.fullname} removed from group successfully'},
                        status=status.HTTP_200_OK)


class StartGroupAPIView(generics.CreateAPIView):
    serializer_class = StartCompletedGroupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_id = serializer.validated_data.get('group_id')

        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({'success': False, "message": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        if group.status == 'continues':
            return Response({'success': False, 'message': 'Group is already started'},
                            status=status.HTTP_400_BAD_REQUEST)

        group.status = 'continues'
        group.started_time = timezone.now()
        group.save()

        students = group.students.all()
        for student in students:
            student.status = 'continues'
            student.save()

        return Response({'success': True, 'message': f'Group {group.title} started successfully'},
                        status=status.HTTP_200_OK)


class CompleteGroupAPIView(generics.CreateAPIView):
    serializer_class = StartCompletedGroupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_id = serializer.validated_data.get('group_id')

        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({'success': False, "message": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        if group.status == 'completed':
            return Response({'success': False, 'message': 'Group is already completed'},
                            status=status.HTTP_400_BAD_REQUEST)

        group.status = 'completed'
        group.started_time = timezone.now()
        group.save()

        students = group.students.all()
        for student in students:
            student.status = 'completed'
            student.save()

        return Response({'success': True, 'message': f'Group {group.title} completed successfully'},
                        status=status.HTTP_200_OK)


class AttachTeacherToGroup(generics.CreateAPIView):
    serializer_class = AttachTeacherSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group_id = serializer.validated_data['group_id']
        mentor_id = serializer.validated_data['mentor_id']

        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({'success': False, 'message': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            mentor = Mentor.objects.get(pk=mentor_id)
        except Mentor.DoesNotExist:
            return Response({'success': False, 'message': 'Mentor not found'}, status=status.HTTP_404_NOT_FOUND)

        if group.mentor is not None:
            return Response({'success': False, 'message': 'Group already has a teacher attached'},
                            status=status.HTTP_400_BAD_REQUEST)

        group.mentor = mentor
        group.save()

        return Response({'success': True, 'message': 'Teacher attached to group successfully'},
                        status=status.HTTP_200_OK)


class ReleaseTeacherFromGroup(generics.CreateAPIView):
    serializer_class = ReleaseTeacherSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group_id = serializer.validated_data['group_id']

        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({'success': False, 'message': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

        if group.mentor is None:
            return Response({'success': False, 'message': 'There is no teacher attached to the group'},
                            status=status.HTTP_400_BAD_REQUEST)

        group.mentor = None
        group.save()

        return Response({'success': True, 'message': 'The teacher was removed from the group'},
                        status=status.HTTP_200_OK)


class AttendanceGroupAPIView(generics.CreateAPIView):
    serializer_class = AttendanceGroupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if self.perform_create(serializer):
                return Response({'success': True, 'message': 'Attendance successfully'},
                                status=status.HTTP_200_OK)
            return Response({'success': False, 'message': "To attend a group, the group must be active"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {
                'success': False,
                'message': "Ma'lumotlar to'liq yuborilmadi!"
            }
            data.update(serializer.errors)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        data = serializer.validated_data
        student_attendance = data.get('students_attendance', {})
        group_id = data.get('group_id')
        group_students = Student.objects.filter(group__id=group_id)

        if not group_students.exists():
            raise serializers.ValidationError({'success': False, 'message': 'Group students not found'})

        group = Group.objects.get(id=group_id)
        if group.status != 'continues':
            return False

        for student in group_students:
            student_id = str(student.id)
            attendance, created = Attendance.objects.get_or_create(student=student, date=timezone.now().date())
            if student_id in student_attendance.keys():
                attendance_status = student_attendance[student_id]
                attendance.attended = attendance_status
                attendance.save()
        return True
