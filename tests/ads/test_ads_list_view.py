import pytest
from rest_framework.status import HTTP_200_OK

from core.serializers import AdSerializer
from tests.factories import AdFactory


class TestAdsListView:

    @pytest.mark.django_db
    def test_get_ads_list_page_1(self, client):
        COUNT = 10
        PAGE_SIZE = 4
        ads = AdFactory.create_batch(COUNT)

        response = client.get('/api/ads/')
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
    def test_get_ads_list_page_2(self, client):
        COUNT = 10
        PAGE_SIZE = 4
        PAGE_NUMBER = 2
        ads = AdFactory.create_batch(COUNT)

        response = client.get(f'/api/ads/?page={PAGE_NUMBER}')
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

        ads_json = AdSerializer(ads[::-1][PAGE_SIZE * (PAGE_NUMBER - 1): PAGE_SIZE * PAGE_NUMBER], many=True).data
        assert results == ads_json, 'Объявления возвращаются в неправильном порядке'

    @pytest.mark.django_db
    def test_get_ads_list_last_page(self, client):
        COUNT = 10
        PAGE_SIZE = 4
        PAGE_NUMBER = COUNT // PAGE_SIZE + 1
        ads = AdFactory.create_batch(COUNT)

        response = client.get(f'/api/ads/?page={PAGE_NUMBER}')
        assert response.status_code == HTTP_200_OK, f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

        data: dict = response.data
        response_keys = {'count', 'next', 'previous', 'results'}
        assert set(data.keys()) == response_keys, 'Возвращаются не те ключи'
        assert data.get('count') == COUNT, \
            f"Возвращается количество записей {data.get('count')}, хотя ожидалось {COUNT}"
        assert data.get('next') is None, 'Есть ссылка на следующую страницу'
        assert data.get('previous') is not None, 'Нет ссылки на предыдущую страницу'

        results_keys = {'title', 'price', 'description', 'image', 'author', 'pk'}
        results = data.get('results')
        assert len(results) == COUNT % PAGE_SIZE, \
            f"На одной странице {len(results)} записей, ожидалось {COUNT % PAGE_SIZE}"
        assert set(results[0].keys()) == results_keys, 'Возвращаются не те ключи'

        ads_json = AdSerializer(ads[::-1][-(COUNT % PAGE_SIZE):], many=True).data
        assert results == ads_json, 'Объявления возвращаются в неправильном порядке'

    @pytest.mark.django_db
    def test_get_ads_list_with_search(self, ad, client):
        COUNT = 1
        TEST_TITLE = 'abcdefgh'

        ad.title = TEST_TITLE
        ad.save()
        ads = AdFactory.create_batch(10)

        response = client.get(f'/api/ads/?title={TEST_TITLE}')
        assert response.status_code == HTTP_200_OK, f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

        data: dict = response.data
        response_keys = {'count', 'next', 'previous', 'results'}
        assert set(data.keys()) == response_keys, 'Возвращаются не те ключи'
        assert data.get('count') == COUNT, \
            f"Возвращается количество записей {data.get('count')}, хотя ожидалось {COUNT}"
        assert data.get('next') is None, 'Есть ссылка на следующую страницу'
        assert data.get('previous') is None, 'Есть ссылка на предыдущую страницу'

        results_keys = {'title', 'price', 'description', 'image', 'author', 'pk'}
        results = data.get('results')
        assert len(results) == COUNT, \
            f"На одной странице {len(results)} записей, ожидалось {COUNT}"
        assert set(results[0].keys()) == results_keys, 'Возвращаются не те ключи'

        ads_json = [AdSerializer(ad).data]
        assert results == ads_json, 'Вернулось не то объявления'
