from rest_framework import serializers
from articles.models import Article

class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['content']