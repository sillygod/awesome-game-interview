import logging

from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework import (viewsets, permissions, status, mixins)

from rest_framework.response import Response

from .serializers import (
    UserCreateSerializer,
    JSONWebTokenSerializerWithEmail,
    UserSerializer,
)

from api.permissions import (IsAuthenticatedOrCreationOrReadOnly, IsSelf)

from api.utils import format_response

logger = logging.getLogger('django')


class UserViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    """

    # which is needed by function list
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticatedOrCreationOrReadOnly,
        IsSelf,
    )

    def get_serializer_class(self):
        """we use rest framework url api versioning
        """
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'login':
            return JSONWebTokenSerializerWithEmail

        return super().get_serializer_class()

    def login(self, request, *args, **kwargs):
        """login with username or mobile and password

        params:
         - name: email
           required: true
           type: string

         - name: password
           required: true
           type: string

        -  name: password2
           required: true
           type: string

        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.object
            serializer = UserSerializer(obj['user'],
                                        context={'request': request})
            data = serializer.data
            data.update({'jwt_token': obj['token']})

            return Response(format_response(200, data=data),
                            status=status.HTTP_200_OK)
        else:
            return Response(format_response(1000, errors=serializer.errors),
                            status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        """create user with email and password

        params:
         - name: email
           required: true
           type: string

         - name: password
           required: true
           type: string

        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            instance = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.initial_data)

            data = UserSerializer(instance, context={'request': request}).data
            # login after creating user
            jwt_serializer = JSONWebTokenSerializerWithEmail(
                data={
                    'email': request.data['email'],
                    'password': request.data['password']
                })
            if not jwt_serializer.is_valid():
                return Response(format_response(1000,
                                                errors=serializer.errors),
                                status=status.HTTP_400_BAD_REQUEST)

            obj = jwt_serializer.object
            data.update({'jwt_token': obj['token']})

            return Response(format_response(200, data=data),
                            status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()

    def partial_update(self, request, *args, **kwargs):
        return Response(format_response(200, data={}),
                        status=status.HTTP_200_OK)
