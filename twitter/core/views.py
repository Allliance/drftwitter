from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import User, Twit, Comment
from .authentication import UserAuthentication
from rest_framework import permissions
from .serializers import UserSerializer, TwitSerializer, CommentSerializer


class DataView(mixins.CreateModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               mixins.RetrieveModelMixin,
               generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserView(DataView):
    authentication_classes = [UserAuthentication]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            token = Token.objects.create(user=User.objects.get(pk=user_serializer.data['id']))
            return Response(data=request.data, status=status.HTTP_201_CREATED, headers={'token': token})
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TwitView(DataView):
    queryset = Twit.objects.all()
    serializer_class = TwitSerializer


class CommentView(DataView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
