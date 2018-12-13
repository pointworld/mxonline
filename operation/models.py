from datetime import datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course


# Create your models here.

class UserConsulting(models.Model):
    """
    用户咨询
    我要学习的表单
    """

    # 用户姓名
    name = models.CharField(max_length=20, verbose_name='name')
    # 手机号
    mobile = models.CharField(max_length=11, verbose_name='mobile')
    # 课程名
    course_name = models.CharField(max_length=50, verbose_name='course name')
    add_time = models.DateTimeField(
        verbose_name='add time',
        default=datetime.now
    )

    class Meta:
        verbose_name = 'user consulting'

    def __str__(self):
        return 'user: {0} mobile: {1}'.format(self.name, self.mobile)


class CourseComments(models.Model):
    """
    用户对课程的评论
    """

    # 涉及两个外键: 用户、课程
    user = models.ForeignKey(UserProfile, verbose_name='user', on_delete='')
    course = models.ForeignKey(Course, verbose_name='course', on_delete='')
    comments = models.CharField(max_length=250, verbose_name='comments')
    add_time = models.DateTimeField(
        verbose_name='add time',
        default=datetime.now
    )

    class Meta:
        verbose_name = 'course comments'
        # verbose_name_plural = verbose_name

    def __str__(self):
        return 'comments of user({0}) to {1}:'.format(self.user, self.course)


class UserFavorite(models.Model):
    """
    用户收藏
    用户对课程、机构或讲师的收藏
    """

    TYPE_CHOICES = (
        # 课程
        (1, 'course'),
        # 课程机构
        (2, 'course_org'),
        # 讲师
        (3, 'teacher'),
    )

    # 用户 id
    user_id = models.IntegerField(default=0)
    # 收藏类型
    fav_type = models.IntegerField(
        choices=TYPE_CHOICES,
        default=1,
        verbose_name='favorite type'
    )
    add_time = models.DateTimeField(
        verbose_name='add time',
        default=datetime.now
    )

    class Meta:
        verbose_name = 'user favorite'

    def __str__(self):
        return 'user({0}) has a collection to {1}'.format(
            self.user_id,
            self.fav_type
        )


class UserMessage(models.Model):
    """
    用户消息
    消息有两种：发给所有用户和发给某一个用户
    """

    RECEIVER_TYPE = (
        (0, 'all_users'),
        (1, 'user')
    )

    receiver = models.IntegerField(
        default=0,
        choices=RECEIVER_TYPE,
        verbose_name='receiver',
    )
    message = models.CharField(max_length=500, verbose_name='message content')
    # 是否已读
    has_read = models.BooleanField(default=False, verbose_name=' has read')
    add_time = models.DateTimeField(
        verbose_name='add time',
        default=datetime.now
    )

    class Meta:
        verbose_name = 'user message'


class UserCourse(models.Model):
    """
    用户学习的课程
    """

    # 涉及两个外键: 用户、课程
    user = models.ForeignKey(UserProfile, verbose_name='user', on_delete='')
    course = models.ForeignKey(Course, verbose_name='course', on_delete='')
    add_time = models.DateTimeField(
        verbose_name='add time',
        default=datetime.now
    )

    class Meta:
        verbose_name = 'user course'

    def __str__(self):
        return 'user({0}) learned <{1}> course'.format(self.user, self.course)
