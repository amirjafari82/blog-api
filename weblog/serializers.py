from rest_framework import serializers
from .models import Article, Category, Comment


class ArticleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Article
        fields = '__all__'
        

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'
        

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = '__all__'
        

class CommentReplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ('body','article')