import pytest
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from tests.factories import UserFactory

from users.serializers import CurrentUserSerializer


class TestUsersListView:

    @pytest.mark.django_db
    def test_users_list_view_by_user(self, client, user_and_access_token):
        COUNT = 10
        PAGE_SIZE = 1

        user, access_token = user_and_access_token
        users = UserFactory.create_batch(COUNT)

        response = client.get(
            '/api/users/',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response.status_code == HTTP_200_OK, f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

        data: dict = response.data
        response_keys = {'count', 'next', 'previous', 'results'}
        assert set(data.keys()) == response_keys, 'Возвращаются не те ключи'
        assert data.get('count') == PAGE_SIZE, \
            f"Возвращается количество записей {data.get('count')}, хотя ожидалось {PAGE_SIZE}"
        assert data.get('next') is None, 'Есть ссылка на следующую страницу'
        assert data.get('previous') is None, 'Есть ссылка на предыдущую страницу'

        results_keys = {'first_name', 'last_name', 'phone', 'email', 'image', 'pk'}
        results = data.get('results')
        assert len(results) == PAGE_SIZE, \
            f"На одной странице {len(results)} записей, ожидалось {PAGE_SIZE}"
        assert set(results[0].keys()) == results_keys, 'Возвращаются не те ключи'

        user_json = CurrentUserSerializer([user], many=True).data
        assert results == user_json, 'Возвращается не тот пользователь'

    @pytest.mark.django_db
    def test_users_list_view_by_admin(self, client, admin_and_access_token):
        COUNT = 10
        PAGE_SIZE = 4

        users = UserFactory.create_batch(COUNT - 1)
        admin, access_token = admin_and_access_token
        users.insert(0, admin)

        response = client.get(
            '/api/users/',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response.status_code == HTTP_200_OK, f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

        data: dict = response.data
        response_keys = {'count', 'next', 'previous', 'results'}
        assert set(data.keys()) == response_keys, 'Возвращаются не те ключи'
        assert data.get('count') == COUNT, \
            f"Возвращается количество записей {data.get('count')}, хотя ожидалось {PAGE_SIZE}"
        assert data.get('next') is not None, 'Нет ссылки на следующую страницу'
        assert data.get('previous') is None, 'Есть ссылка на предыдущую страницу'

        results_keys = {'first_name', 'last_name', 'phone', 'email', 'image', 'pk'}
        results = data.get('results')
        assert len(results) == PAGE_SIZE, \
            f"На одной странице {len(results)} записей, ожидалось {PAGE_SIZE}"
        assert set(results[0].keys()) == results_keys, 'Возвращаются не те ключи'

        users_json = CurrentUserSerializer(users[:PAGE_SIZE], many=True).data
        assert results == users_json, 'Возвращается не тот пользователь'

    @pytest.mark.django_db
    def test_users_list_view_by_user(self, client, access_token):
        # Обращение без токена
        response_1 = client.get(
            '/api/users/',
        )
        assert response_1.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_1.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"

        # Обращение с неверным токеном
        response_2 = client.get(
            '/api/users/',
            HTTP_AUTHORIZATION=access_token + "1",
        )
        assert response_2.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_2.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"
