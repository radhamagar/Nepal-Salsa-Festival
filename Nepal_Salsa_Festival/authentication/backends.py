from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()

        try:
            user = User.objects.get(email=email)
            print(user.check_password(password))
            if user.check_password(password) and not user.is_superuser:
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
