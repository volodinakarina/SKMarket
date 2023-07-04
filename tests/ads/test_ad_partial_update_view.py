import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from core.models import Ad


class TestAdPartialUpdateView:

    @pytest.mark.django_db
    def test_ad_partial_update_view(self, client, ad, user_and_access_token):
        user, access_token = user_and_access_token
        ad.author = user
        ad.save()
        data_list = [
            {'title': 'test title'},
            {'price': 1},
            {'description': 'test description'},
        ]

        for data in data_list:
            response = client.patch(
                f'/api/ads/{ad.pk}/',
                data=data,
                content_type='application/json',
                HTTP_AUTHORIZATION=access_token,
            )
            updated_ad = Ad.objects.get(pk=ad.pk)

            assert response.status_code == HTTP_200_OK, \
                f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

            if 'title' in data:
                assert updated_ad.title == data['title'], 'Название объявления не совпадает с переданным'
            if 'price' in data:
                assert updated_ad.price == data['price'], 'Цена объявления не совпадает с переданной'
            if 'description' in data:
                assert updated_ad.description == data['description'], 'Описание объявления не совпадает с переданным'

            assert updated_ad.author == user, 'Автор объявления не совпадает с переданным'
            assert updated_ad.is_active is True, 'Объявление не активно'

    @pytest.mark.django_db
    def test_ad_partial_update_view_by_admin(self, client, ad, admin_access_token):
        data = {
            'title': 'test title',
            'price': 1,
            'description': 'test description',
        }
        response = client.patch(
            f'/api/ads/{ad.pk}/',
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=admin_access_token,
        )
        updated_ad = Ad.objects.get(pk=ad.pk)

        assert response.status_code == HTTP_200_OK, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

        assert updated_ad.title == data['title'], 'Название объявления не совпадает с переданным'
        assert updated_ad.price == data['price'], 'Цена объявления не совпадает с переданной'
        assert updated_ad.description == data['description'], 'Описание объявления не совпадает с переданным'
        assert updated_ad.author == ad.author, 'Автор объявления обновился'
        assert updated_ad.is_active is True, 'Объявление не активно'

    @pytest.mark.django_db
    def test_partial_update_ad_errors(self, ad, client, user_and_access_token, access_token_2):
        user, access_token = user_and_access_token
        ad.author = user
        ad.save()
        data = {
            'title': 'test title',
            'price': 1,
            'description': 'test description',
        }

        # Обращение без токена
        response_1 = client.patch(
            f'/api/ads/{ad.pk}/',
            data=data,
            content_type='application/json',
        )
        assert response_1.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_1.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"

        # Обращение с пустыми данными:
        data_3 = {
            'title': '',
            'price': '',
            'description': '',
        }
        response_3 = client.patch(
            f'/api/ads/{ad.pk}/',
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
        response_4 = client.patch(
            f'/api/ads/{ad.pk}/',
            data=data_4,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response_4.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_4.status_code}, ожидался {HTTP_400_BAD_REQUEST}"

        response_keys = {'price', }
        assert set(response_4.data.keys()) == response_keys, 'Не возвращается ошибка поля price'

        # Обращение не к своему объявлению
        response_4 = client.patch(
            f'/api/ads/{ad.pk}/',
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token_2,
        )
        assert response_4.status_code == HTTP_403_FORBIDDEN, \
            f"Возвращается статус {response_4.status_code}, ожидался {HTTP_403_FORBIDDEN}"
