from rest_framework import serializers
from .models import User, Twit, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['name', 'username']


class TwitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Twit
        fields = ['text', 'date_modified']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['text']
