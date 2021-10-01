from rest_framework.response import Response
from rest_framework.views import APIView


class UserView(APIView):

    def get(self, request):
        return Response("successful")


class TwitView(APIView):

    def get(self, request):
        return Response("successful")
