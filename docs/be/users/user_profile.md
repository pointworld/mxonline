# 开发 user_profile

用 user_profile 表覆盖 Django 原有的 user 表

## 设计 user_profile 表

- 设计原则：在原有 user 表的基础上新增字段或覆盖某些原有字段

### Django 默认的 user 表的字段

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

### 根据业务扩展 user 表的字段

需要扩展的字段有：
```text
- nickname      : 用户昵称
- birthday      : 用户生日
- gender        : 用户性别
- address       : 用户地址
- mobile        : 用户手机号
- avatar        : 用户头像
```

## 编写 models 实现 users 表

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

## 注册 users 应用

将 users 添加到 settings.py 文件中的 INSTALLED_APPS 中
```text
INSTALLED_APPS = [
    'users',
    ...
]
```

## 重载 AUTH_USER_MODEL

在 settings.py 中加载如下代码
```text
# 此处重载是为了使我们的 UserProfile 生效
AUTH_USER_MODEL = 'users.UserProfile'
```

## 迁移 users 表到 mxonline 数据库