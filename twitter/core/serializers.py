from rest_framework import serializers
from .models import User, Twit, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'name', 'date_joined', 'date_modified')


class TwitSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Twit
        fields = ('id', 'user',  'text', 'date_created', 'date_modified')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    twit = serializers.ReadOnlyField(source="twit.id")

    class Meta:
        model = Comment
        fields = ('id', 'text', 'user', 'twit', 'date_modified')
