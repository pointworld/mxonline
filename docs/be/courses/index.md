# 开发 courses

course 与 lesson 是一对多的关系
course 与 course_resource 是一对多的管理
lesson 与 video 是一对多的关系

结构：
- course --（一对多）--> lesson --（一对多）--> video
- course --（一对多）--> course_resource

一对多或多对一的关系可以用 Django 的外键来实现

* 开发 `course`，用于存放课程相关信息
* 开发 `lesson`，用于存放章节相关信息
* 开发 `video`，用于存放视频相关信息
* 开发 `course_resource`，用于存放课程资源相关信息

## 开发 course

在 courses 的 models 模块下新增如下代码
```text
from datetime import datetime

class Course(models.Model):
    """
    课程基本信息
    """

    DEGREE_CHOICES = (
        ('ele', 'elementary'),
        ('int', 'intermediate'),
        ('adv', 'advanced'),
    )

    # 课程名
    name = models.CharField(max_length=50, verbose_name='course name')
    # 课程描述
    desc = models.CharField(max_length=200, verbose_name='course description')
    # 课程详细信息
    # TextField 允许不输入长度。可以输入到无限大。暂时定义为 TextFiled，之后更新为富文本
    detail = models.TextField(verbose_name='course detail')
    # 课程难度
    degree = models.CharField(max_length=3, choices=DEGREE_CHOICES)
    # 课程总时长
    duration = models.IntegerField(default=0, verbose_name='learning time (minutes)')
    # 学习人数
    student_nums = models.IntegerField(default=0, verbose_name='number of students')
    # 收藏人数
    fav_nums = models.IntegerField(default=0, verbose_name='number of favorites')
    # 课程封面
    cover = models.ImageField(
        max_length='100',
        upload_to='courses/%Y/%m',
        verbose_name='cover'
    )
    # 课程点击数
    hit_nums = models.IntegerField(default=0, verbose_name='number of hits')
    # 课程添加时间
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'course'
        # verbose_name_plural = verbose_name

```

## 开发 lesson

在 courses 的 models 模块下新增如下代码
```text
class Lesson(models.Model):
    """
    章节相关信息
    """

    # 外键：课程
    # 一个课程对应很多章节。所以在章节表中将课程设置为外键
    # 作为一个字段来让我们可以知道这个章节对应那个课程
    course = models.ForeignKey(Course, verbose_name='course', on_delete='')
    # 章节名
    name = models.CharField(max_length=100, verbose_name='lesson name')
    # 添加时间
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'lesson'
        # verbose_name_plural = verbose_name
```

## 开发 video

在 courses 的 models 模块下新增如下代码
```text
class Video(models.Model):
    """
    视频相关信息
    """

    # 外键：章节
    # 因为一个章节对应很多视频。所以在视频表中将章节设置为外键
    # 作为一个字段来存储让我们可以知道这个视频对应哪个章节
    lesson = models.ForeignKey(Lesson, verbose_name='lesson', on_delete='')
    # 视频名
    name = models.CharField(max_length=100, verbose_name='video name')
    # 添加时间
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'video'
        # verbose_name_plural = verbose_name
```

## 开发 course_resource

在 courses 的 models 模块下新增如下代码
```text
class CourseResource(models.Model):
    """
    课程资源相关信息
    """

    # 外键：课程
    # 因为一个课程对应很多资源。所以在课程资源表中将课程设置为外键
    # 作为一个字段来让我们可以知道这个资源对应那个课程
    course = models.ForeignKey(Course, verbose_name='course', on_delete='')
    # 资源名
    name = models.CharField(max_length=100, verbose_name='resource name')
    # 这里定义成文件类型的字段，后台管理系统中会直接生成上传的按钮
    # FileField 也是一个字符串类型，要指定最大长度
    download = models.FileField(
        max_length=100,
        upload_to='course/resource/%Y/%m',
        verbose_name='file resource'
    )
    # 添加时间
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'course resource'
        # verbose_name_plural = verbose_name
```
