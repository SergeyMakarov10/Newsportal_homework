import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_weekly': {
        'task': 'news.tasks.weekly_post',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

# 1ый терминал - python manage.py runserver
# 2ой терминал - celery -A NewsPaper worker -l INFO --pool=solo
# 3ий терминал - celery -A NewsPaper beat -l INFO
# !все должны быть в нужной директории (в этом случае newspaper/newspaper)