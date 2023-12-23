from django.contrib.auth.models import User
from rest_framework import serializers
from django_app import models


class MessageSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()

    class Meta:
        model = models.Messages
        fields = ["message_id", "text", "from_user", "to_user", "date_time", "is_read"]

    def get_from_user(self, obj):
        return obj.from_user.username

    def get_to_user(self, obj):
        return obj.to_user.username
