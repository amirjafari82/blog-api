from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils.encoding import uri_to_iri
from django.utils.text import slugify
from django.core.paginator import Paginator
from .models import Article, Category, Comment, Vote
from .serializers import ArticleSerializer, CategorySerializer, CommentReplySerializer, CommentSerializer



class ArticleListView(APIView):
    
    def get(self, request):
        page_number = request.GET.get("page",1)
        articles = Article.objects.all().order_by("id")
        paginator = Paginator(articles, per_page=6)
        page_obj = paginator.get_page(page_number)
        srz_data = ArticleSerializer(instance=page_obj,many=True)
        return Response(srz_data.data,status=status.HTTP_200_OK)


class ArticleDetailView(APIView):
    
    def get(self, request, slug):
        article = Article.objects.get(slug=uri_to_iri(slug))
        article.views += 1
        article.save()
        srz_data = ArticleSerializer(article)
        return Response(srz_data.data, status.HTTP_200_OK)
    
    
class LikeArticleView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, slug):
        article = Article.objects.get(slug=uri_to_iri(slug))
        vote = Vote.objects.filter(article=article,user=request.user)
        if vote.exists():
            return Response({'message':'Liked Before'},status.HTTP_200_OK)
        else:
            Vote.objects.create(article=article,user=request.user)
            return Response({'message':'Liked'},status.HTTP_200_OK)
    
    
class UnLikeArticleView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, slug):
        article = Article.objects.get(slug=uri_to_iri(slug))
        vote = Vote.objects.get(user=request.user,article=article)
        vote.delete()
        return Response({'message':'UnLiked'},status.HTTP_200_OK)


class CreateArticleView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        srz_data = ArticleSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save(slug=slugify(srz_data.validated_data['title'],allow_unicode=True))
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateArticleView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        article = Article.objects.get(pk=pk)
        srz_data = ArticleSerializer(instance=article, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save(slug=slugify(srz_data.validated_data['title'],allow_unicode=True))
            return Response(srz_data.data,status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteArticleView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.delete()
        return Response({'message':'article deleted'}, status=status.HTTP_200_OK)
    

class CreateCategoryView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        srz_data = CategorySerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data,status.HTTP_201_CREATED)
        return Response(srz_data.errors,status.HTTP_400_BAD_REQUEST)
    

class CategoryArticleListView(APIView):
    
    def get(self, request, category):
        page_number = request.GET.get("page",1)
        category = Category.objects.get(name=category)
        articles = category.category_articles.all()
        paginator = Paginator(articles, per_page=6)
        page_obj = paginator.get_page(page_number)
        srz_data = ArticleSerializer(instance=page_obj,many=True)
        return Response(srz_data.data,status.HTTP_200_OK)
    

class UpdateCategoryView(APIView):
    permission_classes = [IsAdminUser]
    
    def put(self, request, category):
        category = Category.objects.get(name=category)
        srz_data = CategorySerializer(instance=category, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data,status.HTTP_200_OK)
        return Response(srz_data.errors,status.HTTP_400_BAD_REQUEST)
    

class DeleteCategoryView(APIView):
    permission_classes = [IsAdminUser]
    
    def delete(self, request, category):
        category = Category.objects.get(name=category)
        category.delete()
        return Response({'message':'category deleted'},status.HTTP_200_OK)
    
    
class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        srz_data = CommentSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data,status.HTTP_201_CREATED)
        return Response(srz_data.errors,status.HTTP_400_BAD_REQUEST)
    

class DeleteCommentView(APIView):
    permission_classes = [IsAdminUser]
    
    def delete(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response({'message':'comment deleted'})
    
    
class ReplyCommentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        srz_data = CommentReplySerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save(user=request.user,is_reply=True,reply=comment)
            return Response(srz_data.data,status.HTTP_201_CREATED)
        return Response(srz_data.errors,status.HTTP_400_BAD_REQUEST)
    

class CommentArticleView(APIView):
    
    def get(self, request, slug):
        article = Article.objects.get(slug=uri_to_iri(slug))
        comments = article.acomments.filter(is_reply=False)
        srz_data = CommentSerializer(instance=comments,many=True)
        return Response(srz_data.data,status.HTTP_200_OK)
    
    
class ReplyCommentArticleView(APIView):
    
    def get(self, request, slug):
        article = Article.objects.get(slug=uri_to_iri(slug))
        replies = article.acomments.filter(is_reply=True)
        srz_data = CommentSerializer(instance=replies,many=True)
        return Response(srz_data.data,status.HTTP_200_OK)