from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import UserProfile


class CustomBackend(ModelBackend):
    """
    实现用户名，邮箱，手机号均可登录
    继承 ModelBackend 类，重写 authenticate 方法
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get 只能有一个。两个是 get 失败的一种原因，所以这里不用 filter 方法
            user = UserProfile.objects.get(
                Q(username=username) | Q(email=username) | Q(mobile=username)
            )
            if user.check_password(password):
                return user
        except Exception as e:
            return None
