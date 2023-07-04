import pytest
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from users.serializers import CurrentUserSerializer

from tests.factories import UserFactory


class TestUsersProfileIdView:
    @pytest.mark.django_db
    def test_users_profile_id_view_by_own(self, client, user_and_access_token):
        user, access_token = user_and_access_token

        response = client.get(
            f'/api/users/{user.pk}/',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response.status_code == HTTP_200_OK, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

        user_json = CurrentUserSerializer(user).data
        assert response.data == user_json, 'Данные пользователя не совпадают'

    @pytest.mark.django_db
    def test_users_profile_id_view_by_admin(self, client, admin_access_token):
        users = UserFactory.create_batch(3)

        # Обращение к другим пользователям
        for user in users:
            response = client.get(
                f'/api/users/{user.pk}/',
                HTTP_AUTHORIZATION=admin_access_token,
            )
            assert response.status_code == HTTP_200_OK, \
                f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

            user_json = CurrentUserSerializer(user).data
            assert response.data == user_json, 'Данные пользователя не совпадают'

    @pytest.mark.django_db
    def test_users_profile_id_view_by_user(self, client, access_token):
        users = UserFactory.create_batch(3)

        # Обращение к другим пользователям
        for user in users:
            response = client.get(
                f'/api/users/{user.pk}/',
                HTTP_AUTHORIZATION=access_token,
            )
            assert response.status_code == HTTP_404_NOT_FOUND, \
                f"Возвращается статус {response.status_code}, ожидался {HTTP_404_NOT_FOUND}"

    @pytest.mark.django_db
    def test_users_profile_id_view_errors(self, client, user_and_access_token, admin_access_token):
        user, access_token = user_and_access_token

        # Обращение без токена
        response_1 = client.get(
            f'/api/users/{user.pk}/',
        )
        assert response_1.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_1.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"

        # Обращение с неверным токеном
        response_2 = client.get(
            f'/api/users/{user.pk}/',
            HTTP_AUTHORIZATION=access_token + "1",
        )
        assert response_2.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_2.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"

        # Обращение на несуществующий id
        response_3 = client.get(
            f'/api/users/100000000000/',
            HTTP_AUTHORIZATION=admin_access_token,
        )
        assert response_3.status_code == HTTP_404_NOT_FOUND, \
            f"Возвращается статус {response_3.status_code}, ожидался {HTTP_404_NOT_FOUND}"
