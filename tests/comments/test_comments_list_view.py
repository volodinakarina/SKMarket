import pytest
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from tests.factories import CommentFactory

from core.serializers import CommentSerializer


class TestCommentsListView:

    @pytest.mark.django_db
    def test_comments_list_view(self, client, ad, access_token):
        COUNT = 10

        comments = CommentFactory.create_batch(COUNT, ad=ad)
        another_comments = CommentFactory.create_batch(COUNT)

        response = client.get(
            f'/api/ads/{ad.pk}/comments/',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response.status_code == HTTP_200_OK, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

        data: dict = response.data
        response_keys = {'count', 'next', 'previous', 'results'}
        assert set(data.keys()) == response_keys, 'Возвращаются не те ключи'

        results_keys = {'pk', 'text', 'author', 'created_at', 'author_first_name',
                        'author_last_name', 'author_image', 'ad_id'}
        results = data.get('results')
        assert len(results) == COUNT, \
            f"Комментариев {len(results)}, ожидалось {COUNT}"
        assert set(results[0].keys()) == results_keys, 'Возвращаются не те ключи'

        comments_json = CommentSerializer(comments, many=True).data
        assert results == comments_json, 'Возвращается не та информацию о комментариях'

    @pytest.mark.django_db
    def test_comments_list_view_errors(self, client, access_token, ad):
        # Обращение без токена
        response_1 = client.get(
            f'/api/ads/{ad.pk}/comments/',
        )
        assert response_1.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_1.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"

        # Обращение с неверным токеном
        response_2 = client.get(
            f'/api/ads/{ad.pk}/comments/',
            HTTP_AUTHORIZATION=access_token + "1",
        )
        assert response_2.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_2.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"
