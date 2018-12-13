---

.

---

# mxonline

## 项目启动

```text
git clone https://github.com/pointworld/mxonline.git
$ cd mxonline
$ pip install -r requirements.txt
$ python manage.py runserver
```

## 开发环境

- 操作系统:         MacOS@10.13.5
- 开发工具:         PyCharm@2018.03
- 后台语言:         Python@3.7.1
- 后台框架:         Django@2.1.4
- 数据库:           MySQL@5.7
- 数据库管理工具:    Navicat@12.1.13
- 版本管理工具：     Git

## 开发依赖

## 项目结构

```text
mxonline/
    docs/                                 存放项目开发文档
        be/                               存放后端开发文档
            users/
                user_profile.md
                index.md
                email_auth_code.md
                slide.md
            courses/
                index.md
            organization/
                index.md
    mxonline/
        __init__.py
        settings.py
        urls.py
        wsgi.py
    templates/
    courses/                              app: courses
    users/                                app: users
    organization/                         app: organization
    operation/                            app: operation
    venv/
    .gitignore
    manage.py
    PROJECT.md                            项目开发文档
    README.md                             项目简介
    requirements.txt                      管理 Python 依赖
```
