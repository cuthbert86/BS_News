from rest_framework import serializers
from .models import NewsReport


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsReport
        fields = ['headline',
                  'author', 'content', 'todaysDate', 'is_approved', 'photo']
