from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from customer.models import Mentor, Student
from customer.serializers import MentorRetrieveSerializer, \
    MentorSerializer, StudentSerializer, StudentRetrieveSerializer, StudentsExcelSerializer, ExcelFileSerializer
from customer.utils import xlsx_writer


class MentorListAPIView(generics.ListAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('course_id', openapi.IN_QUERY, description="Filter mentors by course ID",
                          type=openapi.TYPE_INTEGER)
    ])
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(status='no_started') | Q(status='continues'))
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('course_id', openapi.IN_QUERY, description="Filter students by course ID",
                          type=openapi.TYPE_INTEGER)
    ])
    def get(self, request, *args, **kwargs):
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
        # group = instance.group
        # instance.group = None
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

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('course_id', openapi.IN_QUERY, description="Filter completed students by course ID",
                          type=openapi.TYPE_INTEGER)
    ])
    def get(self, request, *args, **kwargs):
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

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('course_id', openapi.IN_QUERY, description="Filter deleted students by course ID",
                          type=openapi.TYPE_INTEGER)
    ])
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class StudentsExcelAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExcelFileSerializer

    def get(self, request, *args, **kwargs):
        queryset = Student.objects.filter(Q(status='no_started') | Q(status='continues'))
        serializer_data = StudentsExcelSerializer(queryset, many=True).data
        headers = [
            "ID", "Fullname", "Phone Number", "Parents", "Coming", "School", "Course",
            "Group", "Added Date", "Grant", "Balance", "Status"
        ]
        excel_obj = xlsx_writer(headers, serializer_data)
        return Response(self.serializer_class(excel_obj, context={'request': request}).data, status=200)
