from django.urls import path

from attendance.views import AttendanceListAPIView, AttendanceRetrieveAPIView, \
    AttendanceCreateAPIView

urlpatterns = [
    path('all/', AttendanceListAPIView.as_view(), name='attendance-list'),
    path('create/', AttendanceCreateAPIView.as_view(), name='attendance-create'),
    path('<int:pk>/', AttendanceRetrieveAPIView.as_view(), name='attendance-retrieve'),
    # path('<int:pk>/update', AttendanceUpdateAPIView.as_view(), name='attendance-update'),
]
