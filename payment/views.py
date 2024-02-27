from django.shortcuts import render
from rest_framework import generics

from .models import Payment
from .serializers import PaymentListSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer


class PaymentCreateAPIView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer


class PaymentUpdateAPIView(generics.UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer


class PaymentDeleteAPIView(generics.DestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer
