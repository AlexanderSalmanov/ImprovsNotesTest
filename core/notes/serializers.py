from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Notes


class NotesSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True, write_only=True
    )

    class Meta:
        model = Notes
        fields = ['id', 'title', 'content', 'created_by']
        extra_kwargs = {'created_by': {'write_only': True}}

