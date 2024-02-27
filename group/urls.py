from django.urls import path

from group.views import GroupListAPIView, GroupCreateAPIView, GroupUpdateAPIView, GroupDeleteAPIView, \
    GroupRetrieveAPIView, AddStudentToGroup, RemoveStudentFromGroup, StartGroupAPIView, CompleteGroupAPIView

urlpatterns = [
    path('all/', GroupListAPIView.as_view(), name='group-list'),
    path('create/', GroupCreateAPIView.as_view(), name='group-create'),
    path('<int:pk>/', GroupRetrieveAPIView.as_view(), name='group-retrieve'),
    path('<int:pk>/update/', GroupUpdateAPIView.as_view(), name='group-update'),
    path('<int:pk>/delete/', GroupDeleteAPIView.as_view(), name='group-delete'),

    path('add-student-to-group/', AddStudentToGroup.as_view(), name='add-student-to-group'),
    path('remove-student-from-group/', RemoveStudentFromGroup.as_view(), name='remove-student-from-group'),
    path('start/', StartGroupAPIView.as_view(), name='start-group'),
    path('complete/', CompleteGroupAPIView.as_view(), name='complete-group'),
]
