from django.urls import include, path
from rest_framework import routers

from .views import AdViewSet, CommentViewSet, UserAdsListAPIView

ad_router = routers.SimpleRouter()
ad_router.register('ads', viewset=AdViewSet)

comment_router = routers.SimpleRouter()
comment_router.register('comments', viewset=CommentViewSet)

urlpatterns = [
    path('ads/me/', UserAdsListAPIView.as_view(), name='user_ads'),
    path('ads/<int:ad_pk>/', include(comment_router.urls))
]

urlpatterns += ad_router.urls
