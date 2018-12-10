from django.db import transaction

from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserCreatingSerializer, UserRetrievingSerializer


class SignupAPIView(APIView, CreateModelMixin):

    http_method_names = ('post',)

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        creating_serializer = UserCreatingSerializer(data=request.data)
        creating_serializer.is_valid(raise_exception=True)
        instance = creating_serializer.save()
        headers = self.get_success_headers(creating_serializer.data)
        retrieving_serializer = UserRetrievingSerializer(instance)
        return Response(retrieving_serializer.data,
                        status=status.HTTP_201_CREATED, headers=headers)
