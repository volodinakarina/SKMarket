from factory.django import DjangoModelFactory
from factory import Faker, SubFactory

from core.models import Ad, Comment
from users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    phone = Faker('phone_number')
    email = Faker('email')


class AdFactory(DjangoModelFactory):
    class Meta:
        model = Ad

    title = Faker('sentence', nb_words=4)
    price = Faker('random_number')
    description = Faker('text', max_nb_chars=20)
    author = SubFactory(UserFactory)


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    text = Faker('sentence', nb_words=5)
    author = SubFactory(UserFactory)
    ad = SubFactory(AdFactory)
