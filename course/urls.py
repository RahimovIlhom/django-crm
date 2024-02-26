from django.urls import path

from course.views import (
    CourseListAPIView,
    CourseCreateAPIView,
    CourseRetrieveAPIView,
    CourseUpdateAPIView,
    CourseDeleteAPIView
)

urlpatterns = [
    path('all/', CourseListAPIView.as_view(), name='course-list'),
    path('create/', CourseCreateAPIView.as_view(), name='course-create'),
    path('<int:pk>/', CourseRetrieveAPIView.as_view(), name='course-retrieve'),
    path('<int:pk>/update/', CourseUpdateAPIView.as_view(), name='course-update'),
    path('<int:pk>/delete/', CourseDeleteAPIView.as_view(), name='course-delete'),
]
