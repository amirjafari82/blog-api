from django.db import models
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=30,unique=True)
    
    def __str__(self):
        return self.name


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_articles')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uarticles')
    title = models.CharField(max_length=80)
    slug = models.SlugField(auto_created=True,unique=True,allow_unicode=True,default=None)
    image = models.ImageField(upload_to='',default=None)
    body = models.TextField()
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f'{self.title} - {self.body[:10]}'
    

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='acomments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    body = models.TextField()
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name='reply_comments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.article.title} - {self.body[:20]}'
    

class Vote(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_like')
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='article_like')
    
    def __str__(self):
        return f'{self.user} Liked {self.article.title[:20]}'