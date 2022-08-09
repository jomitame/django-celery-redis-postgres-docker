# from __future__ import absolute_import, unicode_literals

# from celery import shared_task

# @shared_task
# def add(x, y):
#     return x + y

from celery._state import get_current_app

app = get_current_app()

@app.task()
def add(x,y):
    return x+y

@app.task()
def call_prin_after_time(mesagge):
    from .processor import prin_after_time
    prin_after_time(mesagge)