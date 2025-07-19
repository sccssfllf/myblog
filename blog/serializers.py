from rest_framework import serializers
from .models import ModelPost
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    likes = serializers.StringRelatedField(many=True)

    class Meta:
        model = ModelPost
        fields = ['id', 'title', 'slug', 'content', 'author', 'created_at',
                  'updated_at', 'published', 'published_date', 'likes']
