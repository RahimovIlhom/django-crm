from django.urls import path

from .views import (
    PaymentListAPIView,
    PaymentCreateAPIView,
    PaymentRetrieveAPIView,
    PaymentUpdateAPIView,
    PaymentDeleteAPIView,
)


urlpatterns = [
    path('list/', PaymentListAPIView.as_view(), name='payment-list'),
    path('create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment-retrieve'),
    path('<int:pk>/update/', PaymentUpdateAPIView.as_view(), name='payment-update'),
    path('<int:pk>/delete/', PaymentDeleteAPIView.as_view(), name='payment-delete'),
]
