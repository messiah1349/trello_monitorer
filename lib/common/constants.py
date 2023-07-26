import os

TASK_SCHEDULER_HOST = os.getenv('TASK_SCHEDULER_HOST', 'http://127.0.0.1')
TASK_SCHEDULER_PORT = os.getenv('TASK_SCHEDULER_PORT', '5001')
API_KEY = os.getenv('TRELLO_API', None)
TOKEN = os.getenv('TRELLO_TOKEN', None)

lists = [['648ff8b8470180a3a7c4995d', 'backlog'],
 ['648ff8bb624e117850aa5a52', 'to do'],
 ['648ff8c336033571473c832f', 'review'],
 ['648ff8c5c041fe27d955184c', 'done']]