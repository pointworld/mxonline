# 开发 operation

## 设计表

分析需要那些表:
- 用户可以提交我要学习的个人需求
- 学员的课程评论信息
- 收藏：公开课, 授课讲师, 授课机构 
- 用户消息提醒
- 个人中心：我的课程说明、用户和课程之间的学习关系

* 开发 `user_consulting`，用户咨询
* 开发 `course_comments`，用户评论
* 开发 `user_favorite`，用户收藏
* 开发 `user_message`，用户消息
* 开发 `user_course`，用户学习的课程

## 开发 `user_consulting`

在 operation 的 models 模块下新增如下代码
```text
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
```

## 开发 `course_comments`

在 operation 的 models 模块下新增如下代码
```text
class CourseComments(models.Model):
    """
    用户对课程的评论
    """

    # 涉及两个外键: 用户、课程
    user = models.ForeignKey(UserProfile, verbose_name='user', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='course', on_delete=models.CASCADE)
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

```

## 开发 `user_favorite`

在 operation 的 models 模块下新增如下代码
```text
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

```

## 开发 `user_message`

在 operation 的 models 模块下新增如下代码
```text
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

```

## 开发 `user_course`

在 operation 的 models 模块下新增如下代码
```text
class UserCourse(models.Model):
    """
    用户学习的课程
    """

    # 涉及两个外键: 用户、课程
    user = models.ForeignKey(UserProfile, verbose_name='user', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='course', on_delete=models.CASCADE)
    add_time = models.DateTimeField(
        verbose_name='add time',
        default=datetime.now
    )

    class Meta:
        verbose_name = 'user course'

    def __str__(self):
        return 'user({0}) learned <{1}> course'.format(self.user, self.course)

```
