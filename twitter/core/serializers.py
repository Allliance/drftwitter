from rest_framework import serializers
from .models import User, Twit, Comment


class UserSerializer(serializers.ModelSerializer):
    twits = serializers.PrimaryKeyRelatedField(many=True, queryset=Twit.objects.all())

    class Meta:
        model = User
        fields = ('username', 'name', 'date_joined', 'date_modified', 'twits')


class TwitSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Twit
        fields = ('id', 'user',  'text', 'date_created', 'date_modified')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['twit', 'text', 'date_modified']
