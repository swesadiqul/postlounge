from rest_framework import serializers
from blogs.models import *


# Create your serializers here.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'created_at', 'updated_at']
        read_only_fields = ['slug']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'created_at', 'updated_at']
        read_only_fields = ['slug']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'slug', 'featured_image', 'tags', 'category', 'publish_date', 'expiry_date', 'status', 'is_approved', 'author', 'created_at', 'updated_at', 'view_count', 'comment_count']
        read_only_fields = ['id', 'slug', 'publish_date', 'expiry_date', 'status', 'is_approved', 'author',  'created_at', 'updated_at', 'view_count', 'comment_count']

    def validate(self, data):
        if data.get('expiry_date') and data.get('publish_date') and data['expiry_date'] <= data['publish_date']:
            raise serializers.ValidationError("Expiry date must be later than the publish date.")
        return data