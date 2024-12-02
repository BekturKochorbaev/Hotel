from django.urls import path, include
from .views import change_password

urlpatterns = [
    path('change_password/', change_password, name='change_password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]