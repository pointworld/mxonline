# _*_ encoding:utf8 _*_

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    """
    自定义 user 表
    原则：在原有 user 表的基础上新增字段或覆盖某些原有字段
    """
    # 自定义的性别选择规则
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )
    # 昵称
    nickname = models.CharField(max_length=50, verbose_name='nickname', default='')
    # 生日，可以为空
    birthday = models.DateField(verbose_name='birthday', null=True, blank=True)
    # 性别，只能是男或女，默认男
    gender = models.CharField(
        max_length=5,
        verbose_name='gender',
        choices=GENDER_CHOICES,
        default='female',
    )
    # 地址
    address = models.CharField(max_length=100, verbose_name='address', default='')
    # 电话
    mobile = models.CharField(max_length=11, null=True, blank=True)
    # 头像，默认使用 default.png
    # ImageField 实际也是 CharField 所以也要有 max_length
    avatar = models.ImageField(
        max_length=100,
        upload_to='image/%Y/%m',
        default='image/default.png',
    )

    # meta 信息，即后台栏目名
    class Meta:
        verbose_name = 'user info'
        verbose_name_plural = verbose_name

    # 重载 __str__ 方法，打印实例时会打印 username，username 继承自 AbstractUser
    def __str__(self):
        return self.username
