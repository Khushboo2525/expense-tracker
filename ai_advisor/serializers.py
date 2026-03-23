from rest_framework import serializers
from .models import Conversation


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'question', 'answer', 'created_at']
        read_only_fields = ['id', 'answer', 'created_at']