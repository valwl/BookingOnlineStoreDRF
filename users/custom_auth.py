from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, login=None, password=None, **kwargs):
        if login is None:
            return None
        try:
            user = User.objects.get(email=login)
        except User.DoesNotExist:
            try:
                phone_number = User.objects.phone_normalise(login)
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                return None
        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None