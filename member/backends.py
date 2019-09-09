from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class Backend(ModelBackend):
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class EmailPasswordBackend(Backend):
    """Authentication with user's email and password
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user


class UsernamePasswordBackend(Backend):
    """Authentication with user's email and password
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user


class PhonePasswordBackend(Backend):
    """Authentication with user's email and password
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(mobile=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
