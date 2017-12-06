import sys
import os

# Append project root directory to sys path
sys.path.append(os.getcwd())
# setup the environment
SETTINGS = 'demo.settings'
os.environ['DJANGO_SETTINGS_MODULE'] = SETTINGS

import django
django.setup()

from demo import settings
from django.db import transaction
from django.contrib.auth.models import User

@transaction.atomic
def add_user(username):
    try:
        User.objects.create_user(
            username=username, password=settings.USER_PASSWORD)
    except:
        pass

if __name__ == '__main__':
    add_user('omar')
    add_user('rawad')
    add_user('lara')
    add_user('dinesh')
    add_user('abbas')
    add_user('kabbas')
