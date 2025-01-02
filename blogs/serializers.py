from rest_framework import serializers
from blogs.models import *



# Create your serializers here.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'created_at', 'updated_at']
        read_only_fields = ['slug']