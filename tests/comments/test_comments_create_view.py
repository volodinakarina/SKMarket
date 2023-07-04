import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from core.models import Comment


class TestCommentCreateView:
    @pytest.mark.django_db
    def test_comment_create_view(self, client, ad, user_and_access_token):
        user, access_token = user_and_access_token
        data = {
            'text': "test text"
        }

        response = client.post(
            f'/api/ads/{ad.pk}/comments/',
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response.status_code == HTTP_201_CREATED, \
            f"Возвращается статус {response.status_code}, ожидался {HTTP_201_CREATED}"

        comment: Comment = Comment.objects.all()[0]

        assert comment.text == data['text'], 'Неверный текст комментария'
        assert comment.ad == ad, 'Неверный объявление у комментария'
        assert comment.author == user, 'Неверный автор комментария'
        assert comment.created_at is not None, 'Не установлено время публикации'
        assert comment.is_active is True, 'Комментарий не активен'

    @pytest.mark.django_db
    def test_comment_create_errors(self, client, ad, user_and_access_token):
        user, access_token = user_and_access_token
        data = {
            'text': "test text"
        }

        # Обращение без токена
        response_1 = client.post(
            f'/api/ads/{ad.pk}/comments/',
            data=data,
            content_type='application/json',
        )
        assert response_1.status_code == HTTP_401_UNAUTHORIZED, \
            f"Возвращается статус {response_1.status_code}, ожидался {HTTP_401_UNAUTHORIZED}"

        # Обращение без данных
        response_2 = client.post(
            f'/api/ads/{ad.pk}/comments/',
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response_2.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_2.status_code}, ожидался {HTTP_400_BAD_REQUEST}"

        # Обращение с пустыми данными:
        data_3 = {
            'text': "",
        }
        response_3 = client.post(
            f'/api/ads/{ad.pk}/comments/',
            data=data_3,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response_3.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_3.status_code}, ожидался {HTTP_400_BAD_REQUEST}"

        response_keys = {'text', }
        assert set(response_3.data.keys()) == response_keys, 'Возвращается ошибка не всех полей'

        # Обращение к несуществующему объявлению:
        data_4 = {
            'text': "test",
        }
        response_4 = client.post(
            f'/api/ads/10000000/comments/',
            data=data_4,
            content_type='application/json',
            HTTP_AUTHORIZATION=access_token,
        )
        assert response_4.status_code == HTTP_400_BAD_REQUEST, \
            f"Возвращается статус {response_4.status_code}, ожидался {HTTP_400_BAD_REQUEST}"
