import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storefront.settings.dev")

celery = Celery("storefront", broker_connection_retry_on_startup=True)
celery.config_from_object("django.conf:settings", namespace="CELERY")
celery.conf.broker_connection_retry_on_startup = True
celery.autodiscover_tasks()
