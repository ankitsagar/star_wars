# App
from common.services import BaseService
from users.models import User


class UserService(BaseService):
    model = User
