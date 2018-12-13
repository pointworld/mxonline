# 开发 organization

课程是属于机构的, 机构有机构类别，城市，讲师等字段。

* 开发 `CourseOrg`，用于存放课程机构基本信息
* 开发 `Teacher`，用于存放讲师基本信息
* 开发 `CityDict`，用于存放城市信息

## 开发 course_org

在 organization 的 models 模块下新增如下代码
```text
# _*_ coding:utf8 _*_
from datetime import datetime

from django.db import models


# Create your models here.


class CourseOrg(models.Model):
    """
    课程机构
    """

    name = models.CharField(max_length=50, verbose_name='organization name')
    desc = models.TextField(verbose_name='organization description')
    hit_nums = models.IntegerField(default=0, verbose_name='number of hits')
    fav_nums = models.IntegerField(default=0, verbose_name='number of favorites')
    cover = models.ImageField(
        max_length=100,
        upload_to='org/%Y/%m',
        verbose_name='cover'
    )
    address = models.CharField(max_length=150, verbose_name='organization address')
    # 一个城市可以有很多课程机构，通过将 city 设置外键，变成课程机构的一个字段
    # 可以让我们通过机构找到城市
    city = models.ForeignKey(CityDict, verbose_name='city', on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'course organization'
        # verbose_name_plural = verbose_name


```

## 开发 teacher

在 organization 的 models 模块下新增如下代码
```text
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
    age = models.IntegerField(default=0, verbose_name='age')
    gender = models.CharField(default='male', choices=GENDER_CHOICES)
    work_years = models.IntegerField(default=0, verbose_name='years of working')
    company = models.CharField(max_length=50, verbose_name='company')
    post = models.CharField(max_length=50, verbose_name='post')
    style = models.CharField(max_length=50, verbose_name='style')
    hit_nums = models.IntegerField(default=0, verbose_name='number of hits')
    fav_nums = models.IntegerField(default=0, verbose_name='number of favorites')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'teacher'

```

## 开发 city_dict

在 organization 的 models 模块下新增如下代码
```text
class CityDict(models.Model):
    """
    城市字典
    """

    name = models.CharField(max_length=20, verbose_name='city')
    desc = models.CharField(max_length=200, verbose_name='description')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'city'
```

