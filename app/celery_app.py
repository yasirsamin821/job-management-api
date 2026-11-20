from celery import Celery

celery_app = Celery(
    'job_management',
    broker='amqp://guest:guest@localhost:5672//',
    backend='rpc://'
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    enable_utc=True,
    task_track_started=True,
    imports=("app.tasks.csv_tasks",),
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)