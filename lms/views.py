from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.views import APIView
from .models import *
from .serializers import *


class GetUserProfile(APIView):
    pass


class FindUserView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(username='amid')


from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from PIL import Image

class AvatarUploadView(APIView):
    # https://www.goodcode.io/articles/django-rest-framework-file-upload/
    # https://stackoverflow.com/questions/45564130/django-rest-framework-image-upload
    parser_class = (FileUploadParser,)

    def put(self, request, format=None):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        f = request.data['file']
        img = Image.open(f)
        # print(img.name)
        print(f.name)
        temp = UserProfile(user=User.objects.get(username='amid'), avatar=f).save()

        # temp.avatar.save(f.name, f, save=True)
        return Response(status=status.HTTP_201_CREATED)