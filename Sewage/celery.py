from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sewage.settings')

app = Celery('Sewage')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


from celery.schedules import crontab

app.conf.update(
    CELERYBEAT_SCHEDULE={
        'get_failed_callback': {
            'task': 'ding_callback.tasks.crontab_get_failed_callback',
            'schedule': crontab(hour=20, minute=30),
        }
    }
)
