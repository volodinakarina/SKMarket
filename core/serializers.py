from rest_framework import serializers

from .models import Ad, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_first_name = serializers.CharField(source='author.first_name', read_only=True)
    author_last_name = serializers.CharField(source='author.last_name', read_only=True)
    author_image = serializers.SerializerMethodField(read_only=True)

    def get_author_image(self, obj: Comment):
        request = self.context.get('request')
        photo = obj.author.image
        if photo:
            return request.build_absolute_uri(photo.url)
        return None

    class Meta:
        model = Comment
        fields = ['pk', 'text', 'author', 'created_at', 'author_first_name', 'author_last_name', 'ad',
                  'author_image', 'ad_id']
        read_only_fields = ['created_at', 'ad_id']
        extra_kwargs = {
            'ad': {'write_only': True}
        }


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['title', 'price', 'description', 'image', 'author', 'pk']


class AdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['title', 'price', 'description', 'image', 'author', 'pk']
        read_only_fields = ['author', 'pk']


class AdDetailSerializer(serializers.ModelSerializer):
    author_first_name = serializers.CharField(source='author.first_name')
    author_last_name = serializers.CharField(source='author.last_name')
    phone = serializers.CharField(source='author.phone')

    class Meta:
        model = Ad
        fields = ['pk', 'title', 'price', 'description', 'image', 'phone', 'author_first_name', 'author_last_name',
                  'author_id']
        read_only_fields = ['phone', 'author_first_name', 'author_last_name', 'author_id']