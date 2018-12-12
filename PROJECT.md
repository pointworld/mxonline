# Project

## 目标

开发一个在线教育平台（慕学在线网）

## 需求

### 功能组成

- 用户
    - 登录和注册
    - 个人中心
        - 我的课程
        - 我的收藏
        - 我的消息
        - 修改头像、密码、邮箱
        - 找回密码

- 课程
    - 课程列表
    - 课程详情
        - 课程章节信息
        - 课程评论
    - 课程资源下载
    - 观看

- 授课讲师与授课机构
    - 讲师
        - 讲师列表
        - 讲师介绍
        - 讲师排行
            - 人气排序
        - 讲师详情
            - 讲师的所有课程
    - 机构
        - 机构列表
        - 机构排行
        - 机构详情
            - 机构介绍
            - 机构讲师

- 后台管理
    - 日志
    - 权限管理
    - 用户管理
    - 资源管理
    - ...

## 分析

### 模块

- users：用户管理
- course：课程管理
- organization：机构和教师管理
- operation：用户操作管理

## 前端

### 架构

### 设计

### 页面组成

- 首页
    - 顶部快捷导航
        - 注册或登录
        - 全局搜索（公开课、授课教师、授课机构）
    - 导航
        - 首页
        - 公开课
        - 授课教师
        - 授课机构
    - 轮播图
    - 公开课程
    - 课程机构
    - 底部页脚

### 开发

## 后端

### 架构

#### 数据库设计

```text
业务
    apps
        app: 
            models
```

#### 搭建后台管理系统任务

xadmin

### 设计

#### 数据库设计

#### Django app 设计

#### app models 设计

### 开发

#### 搭建开发环境

...

#### 配置环境依赖

##### 配置 MySQL 驱动

- 安装 mysqlclient 依赖
  - 将 mysqlclient 写入到 requirements.txt 文件中，项目根目录下执行命令：`pip install -r requirements.txt`
- 详情参见：[mysqlclient](https://pypi.org/project/mysqlclient/)

##### 在 settings.py 文件中配置 MySQL 数据库

```text
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': 'mxonline',
        'USER': 'root',
        # 更换为你的密码
        'PASSWORD': '1.',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}
```

##### 在 MySQL 数据库中创建 mxonline 数据库

- 在 Navicat 中新建一个名为 mxonline 的 MySQL 数据库

##### 生成 Django 默认数据表

- 项目根目录下分别执行 `python manage.py makemigrations`, `python manage.py migrate` 命令

#### 开发 users app

##### 设计 user 表

- 在 web 开发中，user 表一般是最先被设计的
- 设计原则：在原有 user 表的基础上新增字段或覆盖某些原有字段

###### Django 默认的 user 表的字段

```text
- id            : 主键
- password      : 用户密码
- last_login    : 用户最近一次的登录时间
- is_superuser  : 用户是否是超级用户
- username      : 用户名
- first_name    : 名
- last_name     : 姓
- email         : 用户邮箱
- is_staff      : 是否是员工
- is_active     : 用户是否处于激活状态
- date_joined   : 用户注册时间
```

###### 根据业务扩展 user 表的字段

需要扩展的字段有：
```text
- nickname      : 用户昵称
- birthday      : 用户生日
- gender        : 用户性别
- address       : 用户地址
- mobile        : 用户手机号
- avatar        : 用户头像
```

##### 编写 models 实现 users 表

1. 在 users 的 models 模块下新增如下代码
```text
from django.contrib.auth.models import AbstractUser


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
```

2. ImageField 字段需要用到 pillow 依赖
    - 添加 pillow 到 requirements.txt 文件中
    - 并在项目根路径下执行命令 `python install -r requirements.txt`
    - pillow 是 Python 用来处理图像的一个库，参见: [pillow](https://pypi.org/project/Pillow/)

##### 注册 users 应用

将 users 添加到 settings.py 文件中的 INSTALLED_APPS 中
```text
INSTALLED_APPS = [
    'users',
    ...
]
```

##### 重载 AUTH_USER_MODEL

在 settings.py 中加载如下代码
```text
# 此处重载是为了使我们的 UserProfile 生效
AUTH_USER_MODEL = 'users.UserProfile'
```

##### 迁移 users  表到 mxonline 数据库


## 测试

## 部署

## 上线
