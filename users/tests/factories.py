from django.core.handlers.wsgi import WSGIRequest
from django.test import Client

from users.models import User

import factory


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'John{0}'.format(n))
    token = 'testtoken'

    is_active = True

    class Meta:
        model = User
