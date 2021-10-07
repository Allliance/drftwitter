from rest_framework import serializers
from .models import User, Twit, Comment
import jwt
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'name', 'date_joined', 'date_modified']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    twit = serializers.ReadOnlyField(source="twit.id")

    class Meta:
        model = Comment
        fields = ['id', 'text', 'user', 'twit', 'date_created']
        related_object = 'twit'


class TwitSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Twit
        fields = ['id', 'text', 'comments']


class JWTTokenPermissionSerializer:
    permission_fields = ['delete_user', 'change_name', 'post_twit', 'edit_twit', 'delete_twit', 'post_comment']
    data = {}

    def __init__(self, data):
        for field in self.permission_fields:
            self.data[field] = data.get(field) if data.get(field) is not None else False

    def merge_to_token(self, token):
        for field in self.permission_fields:
            token[field] = self.data[field]
        return token


def decode_jwt(token):
    try:
        decoded_jwt = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms="HS256")
    except jwt.exceptions.DecodeError:
        return None
    return decoded_jwt
