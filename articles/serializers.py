from rest_framework import serializers
from django.utils.timezone import now
from articles.models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        # article은 읽기에서만 is_valid에서 검사를 할 것
        read_only_fields = ("article",)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("article")
        return ret

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'

class ArticleDetailSerializer(ArticleSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
    days_since_created = serializers.SerializerMethodField()

    def get_days_since_created(self, obj):
        return (now() - obj.created_at).days