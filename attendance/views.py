from django.shortcuts import render
from rest_framework import generics

from .models import Attendance
from .pagination import CustomPagination
from .serializers import AttendanceListSerializer, AttendanceRetrieveSerializer


class AttendanceListAPIView(generics.ListAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceListSerializer
    pagination_class = CustomPagination


class AttendanceRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceRetrieveSerializer


class AttendanceUpdateAPIView(generics.UpdateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceRetrieveSerializer

