import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from core.models import Ad
# from factories import AdFactory


class TestAdCreateView:
    @pytest.mark.django_db
    def test_create_ad(self, client, user_and_access_token):
        user, access_token = user_and_access_token
        data = {
            'title': 'test title',
            'price': 1,
            'description': 'test description',
        }

        response = client.post(
            '/api/ads/',
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,
        )

        assert response.status_code == HTTP_201_CREATED, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_201_CREATED}"

        ad = Ad.objects.all()[0]

        assert ad.title == data['title'], 'Название объявления не совпадает с переданным'
        assert ad.price == data['price'], 'Цена объявления не совпадает с переданной'
        assert ad.description == data['description'], 'Описание объявления не совпадает с переданным'
        assert ad.author == user, 'Автор объявления не совпадает с переданным'
        assert ad.is_active, 'Объявление не активно'

    @pytest.mark.django_db
    def test_create_ad_errors(self, client, user_and_access_token):
        user, access_token = user_and_access_token
        data = {
            'title': 'test title',
            'price': 1,
            'description': 'test description',
        }

        # Обращение без токена
        response_1 = client.post(
            '/api/ads/',
            data=data,
            content_type='application/json',
        )
        assert response_1.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_1.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"

        # Обращение без данных
        response_2 = client.post(
            '/api/ads/',
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response_2.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_2.status_code}, ожидался {HTTP_400_BAD_REQUEST}"

        # Обращение с пустыми данными:
        data_3 = {
            'title': '',
            'price': '',
            'description': '',
        }
        response_3 = client.post(
            '/api/ads/',
            data=data_3,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response_3.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_3.status_code}, ожидался {HTTP_400_BAD_REQUEST}"

        response_keys = {'title', 'price', 'description'}
        assert set(response_3.data.keys()) == response_keys, 'Возвращается ошибка не всех полей'

        # Обращение с отрицательной ценой:
        data_4 = {
            'title': 'title',
            'price': -1,
            'description': 'description',
        }
        response_4 = client.post(
            '/api/ads/',
            data=data_4,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response_4.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_4.status_code}, ожидался {HTTP_400_BAD_REQUEST}"

        response_keys = {'price', }
        assert set(response_4.data.keys()) == response_keys, 'Не возвращается ошибка поля price'
