from django.urls import path, re_path
from . import views

app_name = 'weblog'
urlpatterns = [
    path('articles/',views.ArticleListView.as_view(),name='articles'),
    re_path(r'articles/(?P<slug>[^/]+)/?$',views.ArticleDetailView.as_view(),name='article-detail'),
    re_path(r'articles/like/(?P<slug>[^/]+)/?$',views.LikeArticleView.as_view(),name='like-article'),
    re_path(r'articles/unlike/(?P<slug>[^/]+)/?$',views.UnLikeArticleView.as_view(),name='unlike-article'),
    path('create-article/',views.CreateArticleView.as_view(),name='create-article'),
    path('update-article/<int:pk>',views.UpdateArticleView.as_view(),name='update-article'),
    path('delete-article/<int:pk>',views.DeleteArticleView.as_view(),name='delete-article'),
    path('create-category/',views.CreateCategoryView.as_view(),name='create-category'),
    path('category/<str:category>',views.CategoryArticleListView.as_view(),name='category'),
    path('update-category/<str:category>',views.UpdateCategoryView.as_view(),name='update-category'),
    path('delete-category/<str:category>',views.DeleteCategoryView.as_view(),name='delete-category'),
    path('create-comment/',views.CreateCommentView.as_view(),name='create-comment'),
    path('delete-comment/<int:pk>',views.DeleteCommentView.as_view(),name='delete-comment'),
    path('reply-comment/<int:pk>',views.ReplyCommentView.as_view(),name='reply-comment'),
    re_path(r'article-comments/(?P<slug>[^/]+)/?$',views.CommentArticleView.as_view(),name='article-comments'),
    re_path(r'article-replies/(?P<slug>[^/]+)/?$',views.ReplyCommentArticleView.as_view(),name='article-replies'),
]
