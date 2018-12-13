# 开发 email_auth_code

由于这里的邮箱验证码只和用户有关，且功能比较独立，故放在 users 下

## 设计 email_auth_code 表

相关字段
```text
- code          : 验证码
- email         : 邮箱
- send_type     : 发送类型（注册、找回密码）
- send_time     : 发送时间
```

## 编写 models 实现 email_auth_code 表

在 users 的 models 模块下新增如下代码
```text
from datetime import datetime


class EmailAuthCode(models.Model):
    """
    邮箱验证码
    放在 users 下，是因为这里的邮箱验证码只和用户有关，且功能比较独立
    """
    SEND_CHOICES = (
        ('register', 'register'),
        ('forget', 'retrieve password')
    )
    # 验证码
    code = models.CharField(max_length=20, verbose_name='auth code')
    # 邮箱
    email = models.EmailField(max_length=50, verbose_name='email')
    # 发送类型（注册、找回密码）
    send_type = models.CharField(max_length=10, choices=SEND_CHOICES)
    # 发送时间，这里的 now 得去掉 ()，不去掉会根据编译时间。而不是根据实例化时间。
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'email auth code'
        verbose_name_plural = verbose_name

```

## 迁移 users 表到 mxonline 数据库