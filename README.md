---

.

---

# mxonline

使用 Python3.7.x 与 Django2.x 开发的在线教育平台网站: http://edu.pointborn.com

## 项目启动

### clone 和安装相关依赖包

```bash
git clone https://github.com/pointworld/mxonline.git
cd mxonline
pip install -r requirements.txt
```

### 将项目根目录下的 env 文件重命名为 .env，并修改里面的内容

```text
## 数据库相关配置

# MySQL 数据库

DB_MYSQL_NAME=xxx
DB_MYSQL_HOST=xxx
DB_MYSQL_PORT=xxx
DB_MYSQL_USER=xxx
DB_MYSQL_PASSWORD=xxx


## 邮箱相关配置

# QQ 邮箱

# 发送邮件的邮箱，需要配置开通 SMTP
EMAIL_HOST_USER=xxx@qq.com
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD=xxx
# 收件人看到的发件人
EMAIL_FROM = edu.pointborn.com <youremail@qq.com>


## Django 密钥
SECRET_KEY=^$u=oo2&q6l-r0^$fj5rvk^me7cx)83x_8%2d$%k@uyqo31*^5

ALLOWED_HOSTS=

```

> 这里使用了第三方包 [python-decouple](https://github.com/henriquebastos/python-decouple) 来隔离配置

### 创建数据库和迁移数据

1. 在 MySQL 新创建一个 `mxonline` 数据库

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

2. 将项目根目录下的 `mxonline.sql` 文件中的数据导入到 `mxonline` 数据库中

3. 项目中使用了 `celery` 异步发送邮件，用到了 `redis` 数据库，`redis` 的安装和配置请自行 Google or 百度

### 运行

```bash
$ python manage.py runserver
```

在浏览器中访问: http://127.0.0.1:8000/

## 参考

 - [原版视频课程地址:](https://coding.imooc.com/learn/list/78.html)
 - [mtianyan](https://github.com/mtianyan/Mxonline3)

## 有问题，欢迎提 [issue](https://github.com/pointworld/mxonline/issues)
