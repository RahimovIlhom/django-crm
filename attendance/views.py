from django.shortcuts import render
from rest_framework import generics

from .models import Attendance
from .pagination import CustomPagination
from .serializers import AttendanceListSerializer, AttendanceRetrieveSerializer, AttendanceSerializer


class AttendanceListAPIView(generics.ListAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceListSerializer
    pagination_class = CustomPagination


class AttendanceCreateAPIView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class AttendanceRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


# class AttendanceUpdateAPIView(generics.UpdateAPIView):
#     queryset = Attendance.objects.all()
#     serializer_class = AttendanceSerializer

