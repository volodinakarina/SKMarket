# from django.shortcuts import render
#
# # Create your views here.
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .filter import AdFilter
from .models import Ad, Comment
from .permissions import IsOwner
from .serializers import AdDetailSerializer, AdSerializer, CommentSerializer, AdUpdateSerializer


@extend_schema_view(
    list=extend_schema(description="Retrieve all ads", summary="List ads"),
    retrieve=extend_schema(description="Retrieve ad by id", summary="Retrieve ad"),
    create=extend_schema(description="Create new ad", summary="Create ad"),
    update=extend_schema(description="Full ad update", summary="Update ad"),
    partial_update=extend_schema(description="Partial add update", summary="Partial update ad"),
    destroy=extend_schema(description="Delete ad and ad's comments", summary="Delete comments"),
)
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.filter(is_active=True).all()
    serializers = {
        "retrieve": AdDetailSerializer,
        'update': AdUpdateSerializer,
        'partial_update': AdUpdateSerializer,
    }
    default_serializer = AdSerializer
    filterset_class = AdFilter

    def get_permissions(self):
        if self.action in ['list']:
            return [AllowAny()]
        if self.action in ['retrieve', 'create']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]
        return super().get_permissions()

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def retrieve(self, request, *args, **kwargs):
        self.queryset = self.queryset.select_related('author')
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.id
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        item.is_active = False
        item.save()
        comments = Comment.objects.filter(ad=item).all()
        for comment in comments:
            comment.is_active = False
            comment.save()

        return Response({}, status=204)


@extend_schema_view(
    list=extend_schema(description="Retrieve user's ads list", summary="User's ads")
)
class UserAdsListAPIView(ListAPIView):
    queryset = Ad.objects.filter(is_active=True).all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(author=request.user)
        return super().list(request, *args, **kwargs)


class CommentListPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(is_active=True).all()
    serializer_class = CommentSerializer
    pagination_class = CommentListPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ['retrieve', 'create', 'list']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]
        return super().get_permissions()

    @extend_schema(
        description='Retrieve all comments for one ad',
        summary='Comments list for ad'
    )
    def list(self, request, *args, **kwargs):
        ad_id = kwargs['ad_pk']
        self.queryset = self.queryset.filter(ad_id=ad_id)
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description='Create comment for one ad',
        summary='Create comment'
    )
    def create(self, request, *args, **kwargs):
        request.data['ad'] = kwargs['ad_pk']
        request.data['author'] = request.user.id
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description='Retrieve comment',
        summary='Retrieve comment'
    )
    def retrieve(self, request, *args, **kwargs):
        ad_id = kwargs['ad_pk']
        self.queryset = self.queryset.filter(ad_id=ad_id)
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description='Update comment text',
        summary='Update comment'
    )
    def partial_update(self, request, *args, **kwargs):
        ad_id = kwargs['ad_pk']
        self.queryset = self.queryset.filter(ad_id=ad_id)
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description='Delete comment',
        summary='Delete comment'
    )
    def destroy(self, request, *args, **kwargs):
        ad_id = kwargs['ad_pk']
        self.queryset = self.queryset.filter(ad_id=ad_id)
        comment = self.get_object()
        comment.is_active = False
        comment.save()
        return Response({}, status=204)
