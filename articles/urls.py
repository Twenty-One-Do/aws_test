from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    # CBV는 아래처럼 참조하는 방식이 다름
    path("", views.AricleListAPIView.as_view(), name="article_list"),
    path("<int:pk>/",views.ArticleDetailAPIView.as_view(),name="article_detail"),
    path("<int:article_pk>/comments",views.CommentListAPIView.as_view(),name="article_comments"),
    path("comments/<int:pk>", views.CommentDetailAPIView.as_view(),name="comment_detail"),
    path("check-sql/", views.check_sql, name="check_sql"),
]
