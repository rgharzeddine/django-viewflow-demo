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
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Permission, Group


def add_user(username):
    try:
        User.objects.create_user(
            username=username, password=settings.USER_PASSWORD)
    except:
        pass


def add_group(group_name, permission_codes):
    user_ct = ContentType.objects.get_for_model(User)

    try:
        group, _ = Group.objects.get_or_create(name=group_name)
    except:
        pass

    permissions = []
    for code in permission_codes:
        permission, _ = Permission.objects.get_or_create(
            content_type=user_ct,
            codename=code,
            name=code.capitalize().replace('_', ' ')
        )

        permissions.append(permission)

    group.permissions.add(*permissions)


def add_user_to_group(username, group_name):
    user = User.objects.get(username=username)
    group = Group.objects.get(name=group_name)
    user.groups.add(group)


if __name__ == '__main__':
    # create users
    add_user('rawad')
    add_user('lara')
    add_user('dinesh')
    add_user('abbas')
    add_user('kabbas')

    # create a managers group has approval permissions
    add_group('managers', ['can_approve'])

    # create a manager
    add_user('omar')
    add_user_to_group('omar', 'managers')
