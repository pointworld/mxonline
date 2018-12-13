# 开发 slide

轮播图
    是一个比较独立的功能，不会和其他 model 产生关系
    故这里把它放到了 users 中
    TODO: 是否还有更合适的放置位置
    
## 设计 slide 表

相关字段
```text
- title         : 显示名称
- image         : 图片的路径地址
- url           : 幻灯片的跳转
- index         : 幻灯片索引
- add_time      : 该记录的生成时间
```

## 编写 models 实现 slide 表

在 users 的 models 模块下新增如下代码
```text
class Slide(models.Model):
    """
    轮播图
    是一个比较独立的功能，不会和其他 model 产生关系
    故这里把它放到了 users 中
    TODO: 是否还有更合适的放置位置
    """
    
    # 显示名称
    title = models.CharField(max_length=100, verbose_name='title')
    # 图片的路径地址
    image = models.ImageField(
        max_length=100,
        upload_to='slide/%Y/%m',
        verbose_name='slide image'
    )
    # 幻灯片的跳转
    url = models.URLField(max_length=200, verbose_name='access url')
    # 幻灯片索引
    index = models.IntegerField(default=100, verbose_name='index')
    # 该记录的生成时间
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add time')

    class Meta:
        verbose_name = 'slide'
        verbose_name_plural = verbose_name
```

## 迁移 users 表到 mxonline 数据库