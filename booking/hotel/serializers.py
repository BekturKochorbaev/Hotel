from rest_framework import serializers
from .models import *

class ChangePasswordSerializer(serializers.Serializer):
    model = UserProfile
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
