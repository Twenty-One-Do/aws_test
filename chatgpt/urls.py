from django.urls import path
from . import views
urlpatterns = [
    path('post/<int:pk>/ai-comment', views.comment, name='comment'),
]