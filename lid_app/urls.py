from django.urls import path

from lid_app.views import LidListAPIView, LidCreateAPIView, LidRetrieveAPIView, LidUpdateAPIView, LidDeleteAPIView, \
    ContactListAPIView, ContactRetrieveAPIView, ContactCreateAPIView, ContactUpdateAPIView, ContactDeleteAPIView

urlpatterns = [
    path('all/', LidListAPIView.as_view(), name='lid-list'),
    path('create/', LidCreateAPIView.as_view(), name='lid-create'),
    path('<int:pk>/', LidRetrieveAPIView.as_view(), name='lid-detail'),
    path('<int:pk>/update/', LidUpdateAPIView.as_view(), name='lid-update'),
    path('<int:pk>/delete/', LidDeleteAPIView.as_view(), name='lid-delete'),

    path('contact/all/', ContactListAPIView.as_view(), name='contact-all'),
    path('contact/<int:pk>/', ContactRetrieveAPIView.as_view(), name='contact-retrieve'),
    path('contact/create/', ContactCreateAPIView.as_view(), name='contact-create'),
    path('contact/<int:pk>/update/', ContactUpdateAPIView.as_view(), name='contact-update'),
    path('contact/<int:pk>/delete/', ContactDeleteAPIView.as_view(), name='contact-delete'),
]
