from rest_framework import serializers
from .models import User, Twit, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'username']


class TwitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Twit
        fields = ['user', 'text', 'date_modified']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['twit', 'text', 'date_modified']
