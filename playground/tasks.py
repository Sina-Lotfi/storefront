from time import sleep
from celery import shared_task


@shared_task
def sina(message):
    print("sening emails ...")
    print(message)
    sleep(10)
    print("messages sends")
