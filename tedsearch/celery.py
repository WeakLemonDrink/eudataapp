'''
Celery configuration for the `tedsearch` web application
'''


from celery import Celery
from celery.schedules import crontab


app = Celery('tedsearch')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Configure daily tasks
app.conf.beat_schedule = {
    # Executes `get_daily_package_task` every day at 9:02am, 9:04am, 12:02pm, 12:04pm Monday to
    # Friday
    # Task is run twice at each hour to process further if a timeout occurs
    # Task is run at each hour in case daily packages are not published in time (they are
    # normally published at 8am CET)
    'get-daily-package-every-day': {
        'task': 'tasks.tasks.get_daily_package_task',
        'schedule': crontab(minute='2,4', hour='9,12', day_of_week='mon-fri'),
    },
    # Executes `update_lot_search_vector` every day at 9:10am
    'update-lot-search-vector': {
        'task': 'tasks.tasks.update_lot_search_vector',
        'schedule': crontab(minute=10, hour=9),
    },
    # Executes `email_user_notifications` every day at 9:15am, 12:15am Monday to Friday
    # Task is run at each hour in case daily packages are not published in time (they are
    # normally published at 8am CET)
    'email-user-notifications': {
        'task': 'tasks.tasks.email_user_notifications_task',
        'schedule': crontab(minute=15, hour='9,12', day_of_week='mon-fri'),
    },
}
