import pytest
from rest_framework.status import HTTP_200_OK

from tests.factories import AdFactory

from core.serializers import AdSerializer


class TestAdsMeListView:

    @pytest.mark.django_db
    def test_get_ads_me_list_page_1(self, client, user_and_access_token):
        user, access_token = user_and_access_token
        COUNT = 10
        PAGE_SIZE = 4
        ads = AdFactory.create_batch(COUNT, author=user)
        not_user_ads = AdFactory.create_batch(COUNT)

        response = client.get(
            '/api/ads/me/',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response.status_code == HTTP_200_OK, f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

        data: dict = response.data
        response_keys = {'count', 'next', 'previous', 'results'}
        assert set(data.keys()) == response_keys, 'Возвращаются не те ключи'
        assert data.get('count') == COUNT, \
            f"Возвращается количество записей {data.get('count')}, хотя ожидалось {COUNT}"
        assert data.get('next') is not None, 'Нет ссылки на следующую страницу'
        assert data.get('previous') is None, 'Есть ссылка на предыдущую страницу'

        results_keys = {'title', 'price', 'description', 'image', 'author', 'pk'}
        results = data.get('results')
        assert len(results) == PAGE_SIZE, \
            f"На одной странице {len(results)} записей, ожидалось {PAGE_SIZE}"
        assert set(results[0].keys()) == results_keys, 'Возвращаются не те ключи'

        ads_json = AdSerializer(ads[::-1][:PAGE_SIZE], many=True).data
        assert results == ads_json, 'Объявления возвращаются в неправильном порядке'

    @pytest.mark.django_db
    def test_get_ads_me_list_page_2(self, client, user_and_access_token):
        PAGE = 2
        COUNT = 10
        PAGE_SIZE = 4

        user, access_token = user_and_access_token
        ads = AdFactory.create_batch(COUNT, author=user)
        not_user_ads = AdFactory.create_batch(COUNT)

        response = client.get(
            f'/api/ads/me/?page={PAGE}',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response.status_code == HTTP_200_OK, f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

        data: dict = response.data
        response_keys = {'count', 'next', 'previous', 'results'}
        assert set(data.keys()) == response_keys, 'Возвращаются не те ключи'
        assert data.get('count') == COUNT, \
            f"Возвращается количество записей {data.get('count')}, хотя ожидалось {COUNT}"
        assert data.get('next') is not None, 'Нет ссылки на следующую страницу'
        assert data.get('previous') is not None, 'Нет ссылки на предыдущую страницу'

        results_keys = {'title', 'price', 'description', 'image', 'author', 'pk'}
        results = data.get('results')
        assert len(results) == PAGE_SIZE, \
            f"На одной странице {len(results)} записей, ожидалось {PAGE_SIZE}"
        assert set(results[0].keys()) == results_keys, 'Возвращаются не те ключи'

        ads_json = AdSerializer(ads[::-1][PAGE_SIZE * (PAGE - 1): PAGE_SIZE * PAGE], many=True).data
        assert results == ads_json, 'Объявления возвращаются в неправильном порядке'
