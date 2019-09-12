from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    # 自定义的性别选择规则
    GENDER_CHOICES = (
        ("male", "男"),
        ("female", "女")
    )
    # 昵称
    nick_name = models.CharField(max_length=50, verbose_name="昵称", blank=True, default="")
    # 生日，可以为空
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    # 性别 只能男或女，默认女
    gender = models.CharField(
        max_length=6,
        verbose_name="性别",
        choices=GENDER_CHOICES,
        default="female")
    # 地址
    address = models.CharField(max_length=100, default="", blank=True, verbose_name="地址")
    # 电话
    mobile = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        unique=True,
        verbose_name="电话")
    # 头像 默认使用default.png
    image = models.ImageField(
        upload_to="image/%Y/%m",
        default="image/default.png",
        max_length=100,
        verbose_name="头像"
    )

    # meta 信息，即后台栏目名
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    # 重载__str__方法，打印实例会打印username，username为继承自AbstractUser
    def __str__(self):
        return self.username

    # 获取用户未读消息的数量
    def unread_nums(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(has_read=False, user=self.id).count()


class EmailVerifyRecord(models.Model):
    """邮箱验证码 model"""

    SEND_CHOICES = (
        ("register", "注册"),
        ("forget", "找回密码"),
        ("update_email", "修改邮箱"),
    )
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(
        choices=SEND_CHOICES,
        max_length=20,
        verbose_name="验证码类型")
    # 这里的 now 得去掉(),不去掉会根据编译时间。而不是根据实例化时间。
    send_time = models.DateTimeField(
        default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    """轮播图 model"""

    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(
        upload_to="banner/%Y/%m",
        verbose_name="轮播图",
        max_length=100)
    url = models.URLField(max_length=200, verbose_name="访问地址")
    # 默认 index 很大靠后。想要靠前修改 index 值
    index = models.IntegerField(default=100, verbose_name="顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}(位于第{1}位)'.format(self.title, self.index)
