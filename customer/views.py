from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response

from attendance.pagination import CustomPagination
from customer.models import Mentor, Student
from customer.serializers import MentorRetrieveSerializer, \
    MentorSerializer, StudentSerializer, StudentRetrieveSerializer


class MentorListAPIView(generics.ListAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    def get(self, request, *args, **kwargs):
        """
        Filter mentors by course_id. Example: .../api/customer/mentors/all/?course_id={course_id}
        """
        return super().list(request, *args, **kwargs)


class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(status='no_started') | Q(status='continues'))
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    def get(self, request, *args, **kwargs):
        """
        Filter mentors by course_id. Example: .../api/customer/students/all/?course_id={course_id}
        """
        return super().list(request, *args, **kwargs)


class MentorRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorRetrieveSerializer


class StudentRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentRetrieveSerializer


class MentorCreateAPIView(generics.CreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer


class StudentCreateAPIView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class MentorUpdateAPIView(generics.UpdateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer


class StudentUpdateAPIView(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class MentorDeleteAPIView(generics.DestroyAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={'success': True, 'message': "Mentor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class StudentDeleteAPIView(generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        group = instance.group
        instance.group = None
        instance.status = 'deleted'
        instance.save()
        data = {'success': True, 'message': "The student has been removed from the group and added to the deleted list"}
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class StudentCompletedListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(status='completed'))
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    def get(self, request, *args, **kwargs):
        """
        Filter mentors by course_id. Example: .../api/customer/completed/students/?course_id={course_id}
        """
        return super().list(request, *args, **kwargs)


class StudentDeletedListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(status='deleted'))
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    def get(self, request, *args, **kwargs):
        """
        Filter mentors by course_id. Example: .../api/customer/deleted/students/?course_id={course_id}
        """
        return super().list(request, *args, **kwargs)