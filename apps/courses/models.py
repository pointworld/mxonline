from datetime import datetime

from django.db import models

from DjangoUeditor.models import UEditorField
from organization.models import CourseOrg, Teacher


class Course(models.Model):
    """课程信息表"""

    DEGREE_CHOICES = (
        ("cj", "初级"),
        ("zj", "中级"),
        ("gj", "高级")
    )
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构", null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="讲师", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    # 修改imagepath,不能传 y m 进来，不能加斜杠是一个相对路径，相对于 setting 中配置的 media root
    detail = UEditorField(verbose_name="课程详情", width=600, height=300, imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default='')
    is_banner = models.BooleanField(default=False, verbose_name="是否轮播")
    degree = models.CharField(choices=DEGREE_CHOICES, max_length=2, verbose_name="难度")
    # 使用分钟做后台记录(存储最小单位)前台转换
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    # 保存学习人数:点击开始学习才算
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    you_need_know = models.CharField(max_length=300, default="一颗勤学的心是本课程必要前提", verbose_name="课程须知")
    teacher_tell = models.CharField(max_length=300, default="什么都可以学到,按时交作业,不然叫家长", verbose_name="老师告诉你")
    image = models.ImageField(
        upload_to="courses/%Y/%m",
        verbose_name="封面图",
        max_length=100)
    # 保存点击量，点进页面就算
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    category = models.CharField(max_length=20, verbose_name="课程类别", default="后端开发")
    tag = models.CharField(max_length=15, verbose_name="课程标签", default="")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
    章节模型
    一个课程对应很多章节
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》课程的章节 >> {1}'.format(self.course, self.name)


class Video(models.Model):
    """
    每章视频
    一个章节对应很多视频
    """

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="章节")
    url = models.CharField(max_length=200, default="http://blog.pointborn.com/", verbose_name="访问地址")
    name = models.CharField(max_length=100, verbose_name="视频名")
    # 使用分钟做后台记录(存储最小单位)前台转换
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}章节的视频 >> {1}'.format(self.lesson, self.name)


class CourseResource(models.Model):
    """
    课程资源
    一个课程对应很多资源
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="名称")
    # FileField 也是一个字符串类型，要指定最大长度
    download = models.FileField(
        upload_to="course/resource/%Y/%m",
        verbose_name="资源文件",
        max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》课程的资源: {1}'.format(self.course, self.name)
