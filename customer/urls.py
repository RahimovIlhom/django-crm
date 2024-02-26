from django.urls import path

from customer.views import (
    MentorListAPIView,
    MentorRetrieveAPIView,
    MentorCreateAPIView,
    MentorUpdateAPIView,
    MentorDeleteAPIView,
    StudentListAPIView,
    StudentRetrieveAPIView,
    StudentCreateAPIView,
    StudentUpdateAPIView,
    StudentDeleteAPIView,
    StudentCompletedListAPIView, StudentDeletedListAPIView,
)

urlpatterns = [
    path('mentors/all/', MentorListAPIView.as_view(), name='mentors-list'),
    path('mentors/create/', MentorCreateAPIView.as_view(), name='mentor-create'),
    path('mentors/<int:pk>/', MentorRetrieveAPIView.as_view(), name='mentor-detail'),
    path('mentors/<int:pk>/update/', MentorUpdateAPIView.as_view(), name='mentor-update'),
    path('mentors/<int:pk>/delete/', MentorDeleteAPIView.as_view(), name='mentor-delete'),

    path('students/all/', StudentListAPIView.as_view(), name='students-list'),
    path('students/create/', StudentCreateAPIView.as_view(), name='student-create'),
    path('students/<int:pk>/', StudentRetrieveAPIView.as_view(), name='student-detail'),
    path('students/<int:pk>/update/', StudentUpdateAPIView.as_view(), name='student-update'),
    path('students/<int:pk>/delete/', StudentDeleteAPIView.as_view(), name='student-delete'),

    path('completed/students/', StudentCompletedListAPIView.as_view(), name='students-completed'),
    path('deleted/students/', StudentDeletedListAPIView.as_view(), name='students-deleted'),
]
