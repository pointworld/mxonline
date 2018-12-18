# _*_ coding:utf8 _*_

from datetime import datetime

from django.db import models


# Create your models here.

class CityDict(models.Model):
    """
    城市字典
    """

    name = models.CharField(max_length=20, verbose_name='city')
    desc = models.CharField(max_length=200, verbose_name='description')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    """
    课程机构
    """

    CATEGORY_CHOICES = (
        ('pxjg', '培训机构'),
        ('gx', '高校'),
        ('gr', '个人'),
    )

    name = models.CharField(max_length=50, verbose_name='organization name')
    desc = models.TextField(verbose_name='organization description')
    category = models.CharField(
        max_length=20,
        verbose_name='organization category',
        choices=CATEGORY_CHOICES,
        default='pxjg'
    )
    hit_nums = models.IntegerField(default=0, verbose_name='number of hits')
    fav_nums = models.IntegerField(default=0, verbose_name='number of favorites')
    cover = models.ImageField(
        max_length=100,
        upload_to='org/%Y/%m',
        verbose_name='logo'
    )
    address = models.CharField(max_length=150, verbose_name='organization address')
    # 一个城市可以有很多课程机构，通过将 city 设置外键，变成课程机构的一个字段
    # 可以让我们通过机构找到城市
    city = models.ForeignKey(CityDict, verbose_name='city', on_delete=models.CASCADE)
    learners = models.IntegerField(default=0, verbose_name='number of learners')
    course_nums = models.IntegerField(default=0, verbose_name='number of courses')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'Course Organization'
        # verbose_name_plural = verbose_name

    def get_teacher_nums(self):
        """
        获取课程机构的讲师数量
        :return:
        """
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """
    讲师
    """

    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )

    org = models.ForeignKey(CourseOrg, verbose_name='organization', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name='name')
    age = models.IntegerField(default=18, verbose_name='age')
    gender = models.CharField(max_length=10, default='male', choices=GENDER_CHOICES)
    work_years = models.IntegerField(default=0, verbose_name='years of working')
    company = models.CharField(max_length=50, verbose_name='company')
    post = models.CharField(max_length=50, verbose_name='post')
    # 讲师头像
    avatar = models.ImageField(
        max_length=100,
        upload_to='teacher/%Y/%m',
        verbose_name='avatar',
        default=''
    )
    style = models.CharField(max_length=50, verbose_name='style')
    hit_nums = models.IntegerField(default=0, verbose_name='number of hits')
    fav_nums = models.IntegerField(default=0, verbose_name='number of favorites')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'teacher'

    def get_course_nums(self):
        return self.course_set.all().count()

    def __str__(self):
        return self.name
