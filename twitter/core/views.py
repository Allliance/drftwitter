from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import User, Twit, Comment
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth import authenticate, login
from rest_framework.authentication import TokenAuthentication
from .permissions import IsNewUserOrReadOnly, IsUserOrReadOnly
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


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsNewUserOrReadOnly]

    def get(self, request):
        user = Token.objects.get(key=request.headers.get('token')).user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        user = Token.objects.get(key=request.headers.get('token')).user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request):
        user = Token.objects.get(key=request.headers.get('token')).user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            if user.username != serializer.validated_data['username']:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            token = Token.objects.create(user=user)
            authenticate(username=user.username, password=None)
            login(request, user)
            return Response(data=request.data, status=status.HTTP_201_CREATED, headers={'token': token.key})
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TwitDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUserOrReadOnly]
    queryset = Twit.objects.all()
    serializer_class = TwitSerializer


class NewTwitView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUserOrReadOnly]
    queryset = Twit.objects.all()
    serializer_class = TwitSerializer

    def perform_create(self, serializer):
        user = Token.objects.get(key=self.request.headers.get('token')).user
        serializer.save(user=user)


class CommentView(DataView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
