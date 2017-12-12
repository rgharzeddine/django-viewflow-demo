import sys
import os

# Append project root directory to sys path
sys.path.append(os.getcwd())
# setup the environment
SETTINGS = 'demo.settings'
os.environ['DJANGO_SETTINGS_MODULE'] = SETTINGS

import django  # noqa
django.setup()

from demo import settings  # noqa
from django.contrib.contenttypes.models import ContentType  # noqa
from django.contrib.auth.models import User, Permission, Group  # noqa


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
    # create a managers group has approval permissions
    add_group('managers', ['can_approve'])
    add_group('users', ['no_permission'])

    # create a manager
    add_user('omar')
    add_user_to_group('omar', 'managers')

    # create users
    add_user('rawad')
    add_user_to_group('rawad', 'users')
    # add_user('lara')
    # add_user_to_group('lara', 'users')
    # add_user('dinesh')
    # add_user_to_group('dinesh', 'users')
    # add_user('abbas')
    # add_user_to_group('abbas', 'users')
    # add_user('kabbas')
    # add_user_to_group('kabbas', 'users')

    print('fixtures added')
