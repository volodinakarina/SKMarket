import pytest
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from core.models import Comment, Ad


class TestCommentDestroyView:
    @pytest.mark.django_db
    def test_destroy_comment_by_owner(self, client, user_and_access_token, comment):
        user, access_token = user_and_access_token
        comment.author = user
        comment.save()

        ad = comment.ad

        response = client.delete(
            f'/api/ads/{ad.pk}/comments/{comment.pk}/',
            HTTP_AUTHORIZATION=access_token,
        )

        assert response.status_code == HTTP_204_NO_CONTENT, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_204_NO_CONTENT}"

        inactive_comment = Comment.objects.get(pk=comment.pk)
        assert not inactive_comment.is_active, 'Комментарий остался активным'

        active_ad = Ad.objects.get(pk=ad.pk)
        assert active_ad.is_active, 'Объявление стало неактивным'

    @pytest.mark.django_db
    def test_destroy_comment_by_admin(self, client, admin_access_token, comment):
        ad = comment.ad

        response = client.delete(
            f'/api/ads/{ad.pk}/comments/{comment.pk}/',
            HTTP_AUTHORIZATION=admin_access_token,
        )

        assert response.status_code == HTTP_204_NO_CONTENT, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_204_NO_CONTENT}"

        inactive_comment = Comment.objects.get(pk=comment.pk)
        assert not inactive_comment.is_active, 'Комментарий остался активным'

        active_ad = Ad.objects.get(pk=ad.pk)
        assert active_ad.is_active, 'Объявление стало неактивным'

    @pytest.mark.django_db
    def test_destroy_comment_errors(self, client, comment, access_token):
        ad = comment.ad

        # Обращение без токена
        response_1 = client.delete(
            f'/api/ads/{ad.pk}/comments/{comment.pk}/',
        )

        assert response_1.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_1.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"

        # Обращение по несуществующему id объявления
        response_2 = client.delete(
            f'/api/ads/1000000000/comments/{comment.pk}/',
            HTTP_AUTHORIZATION=access_token,
        )

        assert response_2.status_code == HTTP_404_NOT_FOUND, \
            f"Возвращается статус {response_2.status_code}, ожидался {HTTP_404_NOT_FOUND}"

        # Обращение по несуществующему id комментария
        response_2 = client.delete(
            f'/api/ads/{ad.pk}/comments/1000000000/',
            HTTP_AUTHORIZATION=access_token,
        )

        assert response_2.status_code == HTTP_404_NOT_FOUND, \
            f"Возвращается статус {response_2.status_code}, ожидался {HTTP_404_NOT_FOUND}"

        # Удаление чужого комментария
        response_3 = client.delete(
            f'/api/ads/{ad.pk}/comments/{comment.pk}/',
            HTTP_AUTHORIZATION=access_token,
        )

        assert response_3.status_code == HTTP_403_FORBIDDEN, \
            f"Возвращается статус {response_3.status_code}, ожидался {HTTP_403_FORBIDDEN}"
