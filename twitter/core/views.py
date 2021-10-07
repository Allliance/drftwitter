import json
import logging
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
from .permissions import IsUser, UserPermissions, TwitPermissions, CommentPermissions
from .serializers import UserSerializer, TwitSerializer, CommentSerializer, JWTTokenPermissionSerializer, decode_jwt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import JSONParser
from .redis_cache import cache_data, get_user_data

logger = logging.getLogger('views')


def get_user_by_jwt_token(request):
    logger.warning("Request didn't provide normal token authentication. Trying to authenticate using jwt token.")
    decoded_jwt = decode_jwt(request.headers.get('jwt'))
    if decoded_jwt is None:
        logger.error("no valid jwt token found")
        return None
    user_id = decoded_jwt.get('user_id')
    if user_id:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            logger.error("provided jwt token is not valid (invalid user_id)")
            return None
    logger.warning("Request didn't provide normal token authentication. Trying to authenticate using jwt token")
    return None


def get_user_by_token(request, look_for_jwt=True):
    logger.info("Trying to authenticate user with normal token.")
    try:
        if request.headers.get('token'):
            return Token.objects.get(key=request.headers.get('token')).user
    except Token.DoesNotExist:
        logger.error("invalid normal token")
        pass
    finally:
        if not look_for_jwt:
            logger.error("normal token is not valid and no jwt token was provided.")
            raise exceptions.PermissionDenied
        user = get_user_by_jwt_token(request)
        if user is None:
            raise exceptions.PermissionDenied
        logger.info("user has been authorized using jwt token successfully")
        return user


def get_user_by_username(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        logger.warning("no user found matching username")
        raise http.Http404


def get_twit_by_id(twit_id):
    try:
        return Twit.objects.get(id=twit_id)
    except Twit.DoesNotExist:
        logger.warning("no twit found matching twit_id")
        raise http.Http404


class DataView(APIView):

    def get(self, request):
        cached_data = get_user_data('###')
        if cached_data:
            logger.info("cache data has been used for request")
            return http.HttpResponse(cached_data, content_type='application/json')
        logger.info("no cache data available for request, storing cache data for subsequent requests")
        data = json.dumps([dict(twit) for twit in TwitSerializer(Twit.objects.all(), many=True).data])
        cache_data('###', data)
        return http.HttpResponse(data, content_type='application/json')


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermissions]

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


class UserTwitsView(APIView):

    def get(self, request, username):
        cached_data = get_user_data(username)
        if cached_data:
            logger.info("cache data has been used for request")
            return http.HttpResponse(cached_data, content_type='application/json')
        logger.info("no cache data available for request, storing cache data for subsequent requests")
        data = json.dumps([dict(twit) for twit in
                           TwitSerializer(Twit.objects.filter(user=get_user_by_username(username)), many=True).data])
        cache_data(username, data)
        return http.HttpResponse(data, content_type='application/json')


class TwitDetailsView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'twit_id'
    authentication_classes = [TokenAuthentication]
    permission_classes = [TwitPermissions]
    queryset = Twit.objects.all()
    serializer_class = TwitSerializer

    def perform_create(self, serializer):
        user = get_user_by_token(self.request)
        serializer.save(user=user)

    def retrieve(self, request, *args, **kwargs):
        cached_data = get_user_data('#{twit_id}#'.format(twit_id=kwargs['twit_id']))
        if cached_data:
            logger.info("cached data used for request")
            return http.HttpResponse(cached_data, content_type='application/json')
        logger.info("no cache data available for request, storing cache data for subsequent requests")
        data = json.dumps(dict(TwitSerializer(get_twit_by_id(kwargs['twit_id'])).data))
        cache_data('#{twit_id}#'.format(twit_id=kwargs['twit_id']), data)
        return http.HttpResponse(data, content_type='application/json')


class NewTwitView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [TwitPermissions]
    queryset = Twit.objects.all()
    serializer_class = TwitSerializer

    def perform_create(self, serializer):
        user = get_user_by_token(self.request)
        serializer.save(user=user)


class CommentView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CommentPermissions]
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


class TokenView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUser]

    def get(self, request):
        if request.headers.get('jwt') is None:
            logger.warning("no jwt token provided to view permissions")
            return Response("No jwt token found", status=status.HTTP_400_BAD_REQUEST)
        return Response(decode_jwt(request.headers.get('jwt')))

    def post(self, request):
        serializer = JWTTokenPermissionSerializer(JSONParser().parse(request))
        token = RefreshToken.for_user(get_user_by_token(request, False))
        token = serializer.merge_to_token(token)
        return Response({
            'jwt': str(token)
        }, status=status.HTTP_200_OK)

