import pytest
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from core.models import Ad

from tests.factories import CommentFactory

from core.models import Comment


class TestAdDestroyView:
    @pytest.mark.django_db
    def test_destroy_ad_by_owner(self, client, user_and_access_token, ad):
        user, access_token = user_and_access_token
        ad.author = user
        ad.save()
        CommentFactory.create_batch(5, ad=ad)

        response = client.delete(
            f'/api/ads/{ad.pk}/',
            HTTP_AUTHORIZATION=access_token,
        )

        assert response.status_code == HTTP_204_NO_CONTENT, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_204_NO_CONTENT}"

        inactive_ad = Ad.objects.get(pk=ad.pk)
        assert not inactive_ad.is_active, 'Объявление осталось активным'

        inactive_comments = Comment.objects.all()

        for comment in inactive_comments:
            assert not comment.is_active, f'Комментарий {comment.id} осталось активным'

    @pytest.mark.django_db
    def test_destroy_ad_by_admin(self, client, admin_access_token, ad):
        response = client.delete(
            f'/api/ads/{ad.pk}/',
            HTTP_AUTHORIZATION=admin_access_token,
        )

        assert response.status_code == HTTP_204_NO_CONTENT, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_204_NO_CONTENT}"

        inactive_ad = Ad.objects.get(pk=ad.pk)
        assert inactive_ad.is_active is False, 'Объявление осталось активным'

    @pytest.mark.django_db
    def test_destroy_ad_errors(self, client, ad, access_token):
        # Обращение без токена
        response_1 = client.delete(
            f'/api/ads/{ad.pk}/',
        )

        assert response_1.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_1.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"

        # Обращение по несуществующему id
        response_2 = client.delete(
            f'/api/ads/1000000000/',
            HTTP_AUTHORIZATION=access_token,
        )

        assert response_2.status_code == HTTP_404_NOT_FOUND, \
            f"Возвращается статус {response_2.status_code}, ожидался {HTTP_404_NOT_FOUND}"

        # Удаление чужого объявления
        response_3 = client.delete(
            f'/api/ads/{ad.pk}/',
            HTTP_AUTHORIZATION=access_token,
        )

        assert response_3.status_code == HTTP_403_FORBIDDEN, \
            f"Возвращается статус {response_3.status_code}, ожидался {HTTP_403_FORBIDDEN}"
