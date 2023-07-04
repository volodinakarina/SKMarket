import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED


class TestGetAccessTokenByRefresh:

    @pytest.mark.django_db
    def test_get_access_token_by_refresh(self, client, refresh_token):
        data = {
            'refresh': refresh_token,
        }

        response = client.post(
            '/refresh/',
            data=data,
            content_type='application/json',
        )

        assert response.status_code == HTTP_200_OK, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

        response_keys = {'access', 'refresh',}

        assert set(response.data.keys()) == response_keys, 'Не все токены возвращаются'
        assert response.data.get("access") is not None, "Нет access токена"

    @pytest.mark.django_db
    def test_get_access_token_error(self, client, refresh_token, access_token):
        # Обращение без данных
        response_1 = client.post(
            '/refresh/',
            content_type='application/json',
        )
        assert response_1.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_1.status_code}, ожидался {HTTP_400_BAD_REQUEST}"

        response_keys = {'refresh'}
        assert set(response_1.data.keys()) == response_keys, 'Возвращается ошибка не всех полей'

        # Обращение с пустыми данными:
        data_2 = {
            'refresh': '',
        }
        response_2 = client.post(
            '/refresh/',
            data=data_2,
            content_type='application/json',
        )
        assert response_2.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_2.status_code}, ожидался {HTTP_400_BAD_REQUEST}"

        response_keys = {'refresh'}
        assert set(response_2.data.keys()) == response_keys, 'Не возвращается ошибка'

        # Обращение с неверным токеном:
        data_3 = {
            'refresh': refresh_token + '0',
        }
        response_3 = client.post(
            '/refresh/',
            data=data_3,
            content_type='application/json',
        )
        assert response_3.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_3.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"

        response_keys = {'detail', 'code'}
        assert set(response_3.data.keys()) == response_keys, 'Возвращается ошибка не всех полей'
        assert response_3.data['code'] == 'token_not_valid', 'Возвращается неверная ошибка'

        # Обращение с неверным токеном:
        data_4 = {
            'refresh': access_token.split()[1],
        }
        response_4 = client.post(
            '/refresh/',
            data=data_4,
            content_type='application/json',
        )
        assert response_4.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_4.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"

        response_keys = {'detail', 'code'}
        assert set(response_4.data.keys()) == response_keys, 'Возвращается ошибка не всех полей'
        assert response_4.data['code'] == 'token_not_valid', 'Возвращается неверная ошибка'
