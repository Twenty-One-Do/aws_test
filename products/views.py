from django.core.cache import cache
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializer import ProductsSerializer

@api_view(["GET"])
def product_list(requset):
    cache_key = "product_list"
    if not cache.get(cache_key):
        print("cache miss")
        products = Product.objects.all()
        serializer = ProductsSerializer(products, many=True)
        json_response = serializer.data
        cache.set(cache_key, json_response)

    response_data = cache.get(cache_key)
    return Response(response_data)
