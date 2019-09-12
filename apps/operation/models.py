from datetime import datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course


class UserAsk(models.Model):
    """用户我要学习表单"""

    name = models.CharField(max_length=20, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机")
    course_name = models.CharField(max_length=50, verbose_name="课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户: {0} 手机号: {1}'.format(self.name, self.mobile)


class CourseComments(models.Model):
    """用户对于课程评论"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    comments = models.CharField(max_length=250, verbose_name="评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="评论时间")

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})对于《{1}》 评论 :'.format(self.user, self.course)


class UserFavorite(models.Model):
    """用户对于课程,机构，讲师的收藏"""

    TYPE_CHOICES = (
        (1, "课程"),
        (2, "课程机构"),
        (3, "讲师")
    )

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    # course = models.ForeignKey(Course, verbose_name=u"课程")
    # teacher = models.ForeignKey()
    # org = models.ForeignKey()
    # fav_type =

    # 机智版
    # 直接保存用户的 id
    fav_id = models.IntegerField(default=0)
    # 表明收藏的是哪种类型
    fav_type = models.IntegerField(choices=TYPE_CHOICES, default=1, verbose_name="收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="评论时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})收藏了{1} '.format(self.user, self.fav_type)


class UserMessage(models.Model):
    """用户消息表"""

    # 因为我们的消息有两种: 发给全员和发给某一个用户
    # 所以如果使用外键，每个消息会对应要有用户。很难实现全员消息

    # 机智版 为 0 发给所有用户，不为 0 就是发给用户的 id
    user = models.IntegerField(default=0, verbose_name="接收用户")
    message = models.CharField(max_length=500, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})接收了{1} '.format(self.user, self.message)


class UserCourse(models.Model):
    """用户课程表"""

    # 会涉及两个外键: 1. 用户， 2. 课程
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})学习了{1} '.format(self.user, self.course)
