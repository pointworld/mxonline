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
- courses：课程管理
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

根据业务设计所需表的相关字段

```text
users: 
    user_profile
        id, password, last_login, is_superuser, username, first_name, last_name, email,
        is_staff, date_joined, nickname, birthday, gender, address, mobile, avatar
courses:
organization:
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

- 在 web 开发中，user 表一般是最先被设计的
- 设计原则：在原有 user 表的基础上新增字段或覆盖某些原有字段

* [开发 user_profile](docs/be/users/user_profile.md)

#### 开发 courses app

#### 开发 organization app

## 测试

## 部署

## 上线
