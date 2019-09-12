from __future__ import absolute_import

import os

import django

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mxonline.settings')
django.setup()

app = Celery('mxonline')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
