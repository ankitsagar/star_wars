# Django
from django.core.exceptions import ObjectDoesNotExist

# App
from users.models import User


class UserService:

    def get_all_user(self):
        return User.objects.all()

    def get_user_by_id(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            user = None
        return user
