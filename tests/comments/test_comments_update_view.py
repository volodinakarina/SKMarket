import pytest
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, \
    HTTP_404_NOT_FOUND

from core.models import Comment


class TestCommentsUpdateView:

    @pytest.mark.django_db
    def test_comment_update_view_by_owner(self, client, comment, user_and_access_token):
        user, access_token = user_and_access_token

        comment.author = user
        comment.save()

        data = {
            'text': "test text"
        }

        ad = comment.ad

        response = client.patch(
            f'/api/ads/{ad.pk}/comments/{comment.pk}/',
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response.status_code == HTTP_200_OK, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

        updated_comment: Comment = Comment.objects.all()[0]

        assert updated_comment.text == data['text'], 'Неверный текст комментария'
        assert updated_comment.ad == ad, 'Неверное объявление у комментария'
        assert updated_comment.author == user, 'Неверный автор комментария'
        assert updated_comment.created_at is not None, 'Не установлено время публикации'
        assert updated_comment.is_active, 'Комментарий не активен'

    @pytest.mark.django_db
    def test_comment_update_view_by_admin(self, client, comment, admin_and_access_token):
        admin, access_token = admin_and_access_token
        data = {
            'text': "test text"
        }

        ad = comment.ad

        response = client.patch(
            f'/api/ads/{ad.pk}/comments/{comment.pk}/',
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response.status_code == HTTP_200_OK, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_200_OK}"

        updated_comment: Comment = Comment.objects.all()[0]

        assert updated_comment.text == data['text'], 'Неверный текст комментария'
        assert updated_comment.ad == ad, 'Неверное объявление у комментария'
        assert updated_comment.author != admin, 'Автором комментария стал админ'
        assert updated_comment.created_at is not None, 'Не установлено время публикации'
        assert updated_comment.is_active, 'Комментарий не активен'

    @pytest.mark.django_db
    def test_comment_update_view_errors(self, client, comment, user_and_access_token, access_token_2):
        user, access_token = user_and_access_token

        comment.author = user
        comment.save()

        ad = comment.ad

        # Обращение без токена
        data_1 = {
            'text': "test text"
        }
        response_1 = client.patch(
            f'/api/ads/{ad.pk}/comments/{comment.pk}/',
            data=data_1,
            content_type='application/json',
        )
        assert response_1.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_1.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"

        # Обращение с пустыми данными:
        data_2 = {
            'text': '',
        }
        response_2 = client.patch(
            f'/api/ads/{ad.pk}/comments/{comment.pk}/',
            data=data_2,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response_2.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_2.status_code}, ожидался {HTTP_400_BAD_REQUEST}"

        response_keys = {'text', }
        assert set(response_2.data.keys()) == response_keys, 'Возвращается ошибка не всех полей'

        # Обращение к несуществующему объявлению:
        # data_3 = {
        #     'text': "test",
        # }
        # response_3 = client.patch(
        #     f'/api/ads/10000000/comments/{comment.pk}/',
        #     data=data_3,
        #     content_type='application/json',
        #     HTTP_AUTHORIZATION=access_token,
        # )
        # assert response_3.status_code == HTTP_404_NOT_FOUND, \
        #     f"Возвращается статус {response_3.status_code}, ожидался {HTTP_404_NOT_FOUND}"

        # Обращение к несуществующему комментарию:
        data_4 = {
            'text': "test",
        }
        response_4 = client.patch(
            f'/api/ads/{ad.pk}/comments/10000000/',
            data=data_4,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response_4.status_code == HTTP_404_NOT_FOUND, \
            f"Возвращается статус {response_4.status_code}, ожидался {HTTP_404_NOT_FOUND}"

        # Обращение не к чужому комментарию
        data_5 = {
            'text': "test"
        }

        response_5 = client.patch(
            f'/api/ads/{ad.pk}/comments/{comment.pk}/',
            data=data_5,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token_2,
        )

        assert response_5.status_code == HTTP_403_FORBIDDEN, \
            f"Возвращается статус {response_5.status_code}, ожидался {HTTP_403_FORBIDDEN}"
