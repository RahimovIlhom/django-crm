from datetime import datetime

from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from customer.models import Student
from .models import Group
from .serializers import GroupListSerializer, GroupSerializer, GroupRetrieveSerializer, \
    StudentGroupAssignmentSerializer, StartCompletedGroupSerializer


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
            return Response({'success': False, "error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({'success': False, "error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        if student.group == group:
            return Response({'success': False, 'error': 'The student has already joined the specified group'},
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
            return Response({'success': False, "error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({'success': False, "error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        if student.group != group:
            return Response({'success': False, 'error': 'Student is not assigned to the specified group'},
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
            return Response({'success': False, "error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        if group.status == 'continues':
            return Response({'success': False, 'error': 'Group is already started'}, status=status.HTTP_400_BAD_REQUEST)

        group.status = 'continues'
        group.started_time = datetime.now()  # Use datetime.now() to get the current datetime
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
            return Response({'success': False, "error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        if group.status == 'completed':
            return Response({'success': False, 'error': 'Group is already completed'}, status=status.HTTP_400_BAD_REQUEST)

        group.status = 'completed'
        group.started_time = datetime.now()  # Use datetime.now() to get the current datetime
        group.save()

        students = group.students.all()
        for student in students:
            student.status = 'completed'
            student.save()

        return Response({'success': True, 'message': f'Group {group.title} completed successfully'},
                        status=status.HTTP_200_OK)
