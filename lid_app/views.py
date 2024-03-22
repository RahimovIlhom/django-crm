from django.db.models import Q
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from attendance.pagination import CustomPagination
from lid_app.models import Lid
from lid_app.serializers import LidSerializer


class LidListAPIView(generics.ListAPIView):
    queryset = Lid.objects.all()
    serializer_class = LidSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(status='no_started'))
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('course_id', openapi.IN_QUERY, description="Filter lids by course ID",
                          type=openapi.TYPE_INTEGER)
    ])
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class LidCreateAPIView(generics.CreateAPIView):
    queryset = Lid.objects.all()
    serializer_class = LidSerializer


class LidRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lid.objects.all()
    serializer_class = LidSerializer


class LidUpdateAPIView(generics.UpdateAPIView):
    queryset = Lid.objects.all()
    serializer_class = LidSerializer


class LidDeleteAPIView(generics.DestroyAPIView):
    queryset = Lid.objects.all()
    serializer_class = LidSerializer
