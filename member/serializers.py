import importlib
import re
import string
from django.contrib.auth import (get_user_model, authenticate)

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from rest_framework import serializers

from rest_framework_jwt.compat import (Serializer, get_username_field,
                                       PasswordField)
from rest_framework_jwt.settings import api_settings
from rest_framework.relations import RelatedField

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class JSONWebTokenSerializerWithEmail(Serializer):
    """a customize jwt serializer use email and password.
    """

    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField(write_only=True)

    @property
    def username_field(self):
        return get_username_field()

    def validate(self, attrs):
        credentials = {
            'username': attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg, 1000)

                payload = jwt_payload_handler(user)

                return {'token': jwt_encode_handler(payload), 'user': user}
            else:
                msg = _('Unable to login with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.fields['email'])
            raise serializers.ValidationError(msg, 1000)


class UserCreateSerializer(serializers.ModelSerializer):
    """handle user creation validation
    """

    username = serializers.CharField(max_length=20,
                                     min_length=6,
                                     error_messages={
                                         'blank': 'password can not be empty',
                                         'min_length': 'password is too short'
                                     })

    password = serializers.CharField(max_length=20,
                                     min_length=6,
                                     error_messages={
                                         'blank': 'password can not be empty',
                                         'min_length': 'password is too short'
                                     })
    password2 = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'last_name', 'first_name', 'email',
                  'mobile', 'password', 'password2')

    def validate_username(self, value):
        if value[0] not in string.ascii_letters:
            raise serializers.ValidationError(
                'username should start with letters')
        return value

    def validate_mobile(self, value):
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('this email has been registered',
                                              1004)
        return value

    def validate_password2(self, value):
        if value != self.initial_data['password']:
            raise serializers.ValidationError('password is not consistent',
                                              1001)

    def create(self, validated_data):
        validated_data.pop('password2')
        instance = User.objects.create_user(**validated_data)
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'token',
            'username',
            'email',
        )
