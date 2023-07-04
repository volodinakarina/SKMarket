import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED


class TestGetAccessToken:

    @pytest.mark.django_db
    def test_get_access_token(self, client, user_with_password):
        user, password = user_with_password
        data = {
            'email': user.email,
            'password': password
        }

        response = client.post(
            '/api/token/',
            data=data,
            content_type='application/json',
        )

        assert response.status_code == HTTP_200_OK, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

        response_keys = {'refresh', 'access'}

        assert set(response.data.keys()) == response_keys, 'Не все токены возвращаются'
        assert response.data.get("access") is not None, "Нет access токена"
        assert response.data.get("refresh") is not None, "Нет refresh токена"

    @pytest.mark.django_db
    def test_get_access_token_error(self, client, user_with_password):
        user, password = user_with_password

        # Обращение без данных
        response_1 = client.post(
            '/api/token/',
            content_type='application/json',
        )
        assert response_1.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_1.status_code}, ожидался {HTTP_400_BAD_REQUEST}"

        response_keys = {'email', 'password'}
        assert set(response_1.data.keys()) == response_keys, 'Возвращается ошибка не всех полей'

        # Обращение с пустыми данными:
        data_2 = {
            'email': '',
            'password': '',
        }
        response_2 = client.post(
            '/api/token/',
            data=data_2,
            content_type='application/json',
        )
        assert response_2.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_2.status_code}, ожидался {HTTP_400_BAD_REQUEST}"

        response_keys = {'email', 'password'}
        assert set(response_2.data.keys()) == response_keys, 'Возвращается ошибка не всех полей'

        # Обращение с неверными данными:
        data_3 = {
            'email': user.email,
            'password': password + '1',
        }
        response_3 = client.post(
            '/api/token/',
            data=data_3,
            content_type='application/json',
        )
        assert response_3.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_3.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"

        response_keys = {'detail', }
        assert set(response_3.data.keys()) == response_keys, 'Возвращается ошибка не всех полей'
