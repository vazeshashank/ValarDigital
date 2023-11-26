from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import logging


User = get_user_model()

class CustomUserAuth(ModelBackend):
    def custom_authenticate(self, username, password, user_type):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            print("User does not exist")
            return None

        if user.check_password(password) and user.user_type == user_type:
            user.backend = "django.contrib.auth.backends.ModelBackend"
            return user 
        return None
 #"customAuth.CustomUserAuth"
      

    