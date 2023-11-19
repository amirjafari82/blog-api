from django.contrib import admin
from .models import Article, Category, Comment, Vote

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','views')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Vote)