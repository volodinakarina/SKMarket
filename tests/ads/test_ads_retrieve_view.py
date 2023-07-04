import pytest
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from tests.factories import AdFactory

from core.serializers import AdDetailSerializer


class TestRetrieveView:
    @pytest.mark.django_db
    def test_get_ad_retrieve(self, client, ad, access_token):
        COUNT = 5
        ads = AdFactory.create_batch(COUNT)

        response = client.get(
            f'/api/ads/{ad.pk}/',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response.status_code == HTTP_200_OK, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

        ad_json = AdDetailSerializer(ad).data
        assert response.data == ad_json, f'Возвращаются неверные данные'

    @pytest.mark.django_db
    def test_get_ad_retrieve_errors(self, client, ad, access_token):
        # Обращение без токена
        response_1 = client.get(
            f'/api/ads/{ad.pk}/',
        )

        assert response_1.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_1.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"

        # Обращение по несуществующему id
        response_2 = client.get(
            f'/api/ads/1000000000/',
            HTTP_AUTHORIZATION=access_token,
        )

        assert response_2.status_code == HTTP_404_NOT_FOUND, \
            f"Возвращается статус {response_2.status_code}, ожидался {HTTP_404_NOT_FOUND}"
