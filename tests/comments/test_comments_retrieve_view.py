import pytest
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from core.serializers import CommentSerializer


class TestCommentsRetrieveView:
    @pytest.mark.django_db
    def test_get_comment_retrieve(self, client, comment, access_token):
        response = client.get(
            f'/api/ads/{comment.ad.pk}/comments/{comment.pk}/',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response.status_code == HTTP_200_OK, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

        comment_json = CommentSerializer(comment).data
        assert response.data == comment_json, f'Возвращаются неверные данные'

    @pytest.mark.django_db
    def test_get_comment_retrieve_errors(self, client, comment, access_token):
        # Обращение без токена
        response_1 = client.get(
            f'/api/ads/{comment.ad.pk}/comments/{comment.pk}/',
        )

        assert response_1.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_1.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"

        # # Обращение по неверному id объявления
        response_2 = client.get(
            f'/api/ads/100000000/comments/{comment.pk}/',
            HTTP_AUTHORIZATION=access_token,
        )

        assert response_2.status_code == HTTP_404_NOT_FOUND, \
            f"Возвращается статус {response_2.status_code}, ожидался {HTTP_404_NOT_FOUND}"

        # Обращение по неверному id объявления
        response_3 = client.get(
            f'/api/ads/{comment.ad.pk}/comments/1000000000/',
            HTTP_AUTHORIZATION=access_token,
        )

        assert response_3.status_code == HTTP_404_NOT_FOUND, \
            f"Возвращается статус {response_3.status_code}, ожидался {HTTP_404_NOT_FOUND}"
