import django.core.exceptions
from rest_framework import generics
from django import http
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.core import exceptions
from rest_framework import status
from .models import User, Twit, Comment
from django.contrib.auth import authenticate, login
from rest_framework.authentication import TokenAuthentication
from .permissions import IsUserOrPosting, IsUserOrReadOnly, IsUser
from .serializers import UserSerializer, TwitSerializer, CommentSerializer


def get_user_by_token(request):
    try:
        return Token.objects.get(key=request.headers.get('token')).user
    except Token.DoesNotExist:
        print("fuck")
        raise exceptions.PermissionDenied


def get_user_by_username(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        raise http.Http404


def get_twit_by_id(twit_id):
    try:
        return Twit.objects.get(id=twit_id)
    except Twit.DoesNotExist:
        raise http.Http404


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUserOrPosting]

    def delete(self, request):
        user = get_user_by_token(request)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request):
        user = get_user_by_token(request)
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


class UserTwitsView(generics.ListAPIView):
    serializer_class = TwitSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = Twit.objects.filter(user=get_user_by_username(kwargs['username']))
        return self.list(request, args, kwargs)


class TwitDetailsView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'twit_id'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUserOrReadOnly]
    queryset = Twit.objects.all()
    serializer_class = TwitSerializer

    def get(self, request, *args, **kwargs):
        print('dafuck')
        return self.retrieve(request, args, kwargs)

    def perform_create(self, serializer):
        user = get_user_by_token(self.request)
        serializer.save(user=user)


class NewTwitView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUser]
    queryset = Twit.objects.all()
    serializer_class = TwitSerializer

    def perform_create(self, serializer):
        user = get_user_by_token(self.request)
        serializer.save(user=user)


class CommentView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUserOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    twit = None
    user = None

    def perform_create(self, serializer):
        serializer.save(twit=self.twit, user=self.user)

    def post(self, request, *args, **kwargs):
        self.twit = get_twit_by_id(kwargs['twit_id'])
        self.user = get_user_by_token(self.request)
        return self.create(request, args, kwargs)

    def get(self, request, *args, **kwargs):
        self.queryset = Comment.objects.filter(twit=get_twit_by_id(kwargs['twit_id']))
        return self.list(request, args, kwargs)

