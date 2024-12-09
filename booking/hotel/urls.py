from django.urls import path, include
from .views import change_password, HotelViewSet, RoomViewSet, BookingViewSet

urlpatterns = [
    path('change_password/', change_password, name='change_password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('hotel/', HotelViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='hotel_list'),
    path('hotel/<int:pk>/', HotelViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='hotel_detail'),
    path('room/', RoomViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='room_list'),
    path('room/<int:pk>/', RoomViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='room_detail'),
    path('booking/', BookingViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='booking_list'),
    path('booking/<int:pk>/', BookingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='booking_detail'),
]