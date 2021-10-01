from rest_framework import generics
from rest_framework import mixins
from .models import User, Twit, Comment
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
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TwitView(DataView):
    queryset = Twit.objects.all()
    serializer_class = TwitSerializer


class CommentView(DataView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
