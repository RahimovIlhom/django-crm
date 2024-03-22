from django.urls import path

from lid_app.views import LidListAPIView, LidCreateAPIView, LidRetrieveAPIView, LidUpdateAPIView, LidDeleteAPIView

urlpatterns = [
    path('all/', LidListAPIView.as_view(), name='students-list'),
    path('create/', LidCreateAPIView.as_view(), name='student-create'),
    path('<int:pk>/', LidRetrieveAPIView.as_view(), name='student-detail'),
    path('<int:pk>/update/', LidUpdateAPIView.as_view(), name='student-update'),
    path('<int:pk>/delete/', LidDeleteAPIView.as_view(), name='student-delete'),
]
