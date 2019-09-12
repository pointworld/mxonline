import os
import sys

from decouple import config


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

SECRET_KEY = config('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['*']

# 设置邮箱、手机号和用户名均可登录
AUTHENTICATION_BACKENDS = (
    'users.utils.CustomBackend',
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users',
    'courses',
    'operation',
    'organization',

    'xadmin',
    'crispy_forms',
    'captcha',
    'pure_pagination',
    'DjangoUeditor',
]

# 此处重载是为了使我们的 UserProfile 生效
AUTH_USER_MODEL = "users.UserProfile"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mxonline.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.i18n",
                'django.template.context_processors.media',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'mxonline.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_MYSQL_NAME'),
        'USER': config('DB_MYSQL_USER'),
        'PASSWORD': config('DB_MYSQL_PASSWORD'),
        'HOST': config('DB_MYSQL_HOST'),
        'PORT': config('DB_MYSQL_PORT', default=3306, cast=int),
        'OPTIONS': {'charset': 'utf8', 'init_command': 'SET default_storage_engine=INNODB;'},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'zh-hans'

# 时区改为上海
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# 数据库存储使用时间，True时间会被存为UTC的时间
USE_TZ = False

# 指定的是：每个 APP 里面的静态资源目录
STATIC_URL = '/static/'

# STATICFILES = os.path.join(BASE_DIR, 'static')

# 存放公共静态资源文件
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

## 发送邮件的 setting 设置

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# smtp 服务地址
EMAIL_HOST = "smtp.qq.com"

EMAIL_PORT = 465
# 发送邮件的邮箱，需要配置开通 SMTP
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

EMAIL_USE_SSL = True
# 收件人看到的发件人
EMAIL_FROM = config('EMAIL_FROM')

# 设置我们上传文件的路径

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if not DEBUG:
    # 将分散静态资源文件，收集到统一的位置
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Broker 配置，使用 Redis 作为消息中间件
BROKER_URL = 'redis://localhost:6379/0'
BROKER_TRANSPORT = 'redis'

# Backend 设置，使用 Redis 作为后端结果存储
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_ENABLE_UTC = False

# 防止任务死锁
CELERYD_FORCE_EXECV = True

# 并发的 worker 数量
CELERYD_CONCURRENCY = 8

CELERY_ACKS_LATE = True

# 每个 worker 最多执行的任务数
CELERYD_MAX_TASKS_PER_CHILD = 100

# 任务超时时间
CELERYD_TASK_TIME_LIMIT = 15 * 60
