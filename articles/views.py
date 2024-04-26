from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import (ArticleSerializer,
                          CommentSerializer,
                          ArticleDetailSerializer)
from .models import Article, Comment


class AricleListAPIView(APIView):

    # permission_classes 변수 오버라이딩
    # 이걸 명시하면 이제부터 이 클래스 뷰는 요청 헤더의 Authorization에 유효한 access 토큰이 있어야만 들어올 수 있음
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        # 세션 DB를 사용한게 아니지만 평소처럼 request.user로 현재 유저를 참조할 수 있음
        print(f"\n\n 현재 유저네임: {request.user.username}\n\n")
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        # raise_exception=True 이걸 하면 else문의 코드가 없어도 됨
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # 그냥 숫자 201을 쓰면 너무 가독성이 떨어지니까 status를 통해 명시적으로 나타냄
        else:
            return Response(serializer.errors, status=400)  # bad request

class ArticleDetailAPIView(APIView):

    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self,request,pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    def put(self,request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentListAPIView(APIView):

    def get(self, request, article_pk):
        # 정참조를 하는 방법
        comments = Comment.objects.filter(article_id=article_pk)
        # 역참조를 하는 방법
        article = get_object_or_404(Article, pk=article_pk)
        comments = article.comment_set.all()

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=400)

class CommentDetailAPIView(APIView):

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def check_sql(request):



    # comments = Comment.objects.all().select_related('article')
    # for comment in comments:
    #     print(comment.article.title)
    # print(connection.queries)

    articles = Article.objects.all().prefetch_related('comments')
    for article in articles:
        comments = article.comments.all()
        print(comments)

    return Response(status=status.HTTP_200_OK)