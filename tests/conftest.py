import pytest
from pytest_factoryboy import register
from rest_framework_simplejwt.tokens import RefreshToken

from tests.factories import UserFactory, AdFactory, CommentFactory

register(UserFactory)
register(AdFactory)
register(CommentFactory)


@pytest.fixture
def password():
    return 'T1E2s3t4'


@pytest.fixture
@pytest.mark.django_db
def user_with_password(password):
    user = UserFactory()
    user.set_password(password)
    user.save()
    return user, password


@pytest.fixture
@pytest.mark.django_db
def access_token(user_with_password):
    user, _ = user_with_password
    refresh = RefreshToken.for_user(user)

    return f'Bearer {str(refresh.access_token)}'


@pytest.fixture
@pytest.mark.django_db
def access_token_2(user_with_password, password):
    user = UserFactory()
    refresh = RefreshToken.for_user(user)

    return f'Bearer {str(refresh.access_token)}'


@pytest.fixture
@pytest.mark.django_db
def admin_access_token():
    user = UserFactory()
    user.role = 'admin'
    user.is_staff = True
    user.save()
    refresh = RefreshToken.for_user(user)

    return f'Bearer {str(refresh.access_token)}'


@pytest.fixture
@pytest.mark.django_db
def admin_and_access_token():
    user = UserFactory()
    user.role = 'admin'
    user.is_staff = True
    user.save()
    refresh = RefreshToken.for_user(user)

    return user, f'Bearer {str(refresh.access_token)}'


@pytest.fixture
@pytest.mark.django_db
def user_and_access_token(user_with_password):
    user, _ = user_with_password
    refresh = RefreshToken.for_user(user)

    return user, f'Bearer {str(refresh.access_token)}'


@pytest.fixture
@pytest.mark.django_db
def refresh_token(user_with_password):
    user, _ = user_with_password
    refresh = RefreshToken.for_user(user)

    return str(refresh)
