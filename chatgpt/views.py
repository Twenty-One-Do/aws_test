from django.shortcuts import render
from openai_test import ask_question
from django.shortcuts import get_object_or_404
from articles.models import Article
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ContentSerializer

@api_view(['GET'])
def comment(request, pk):
    content_ins = get_object_or_404(Article, id=pk)
    content = ContentSerializer(content_ins, many=False).data.get('content')
    ans = ask_question(content)
    response = {'comment': ans}
    return Response(response)

