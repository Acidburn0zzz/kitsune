import random
from string import letters
from sumo.tests import LocalizingClient, TestCase, with_save

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from users.models import Profile


class TestCaseBase(TestCase):
    """Base TestCase for the users app test cases."""

    client_class = LocalizingClient


# TODO(Erik): Remove the positional argument. If no users is passed, make one.
def profile(user, **kwargs):
    """Return a saved profile for a given user."""
    defaults = {'user': user, 'name': 'Test K. User', 'bio': 'Some bio.',
                'website': 'http://support.mozilla.com',
                'timezone': None, 'country': 'US', 'city': 'Mountain View'}
    defaults.update(kwargs)

    p = Profile(**defaults)
    p.save()
    return p


@with_save
def user(**kwargs):
    """Return a user with all necessary defaults filled in.

    Default password is 'testpass' unless you say otherwise in a kwarg.

    """
    defaults = {}
    if 'username' not in kwargs:
        defaults['username'] = ''.join(random.choice(letters)
                                       for x in xrange(15))
    defaults.update(kwargs)
    user = User(**defaults)
    user.set_password(kwargs.get('password', 'testpass'))
    return user


def get_user(username='jsocol'):
    """Return a saved Django user, creating one first if necessary."""
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return user(username=username, save=True)


@with_save
def group(**kwargs):
    defaults = {}
    if 'name' not in kwargs:
        defaults['name'] = ''.join(random.choice(letters) for x in xrange(15))
    defaults.update(kwargs)
    return Group(**defaults)


def add_permission(user, model, permission_codename):
    """Add a permission to a user.

    Creates the permission if it doesn't exist.

    """
    content_type = ContentType.objects.get_for_model(model)
    try:
        permission = Permission.objects.get(codename=permission_codename,
                                            content_type=content_type)
    except Permission.DoesNotExist:
        permission = Permission.objects.create(codename=permission_codename,
                                               name=permission_codename,
                                               content_type=content_type)
    user.user_permissions.add(permission)
