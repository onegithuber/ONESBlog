from django.db import models
from django.contrib import admin
class ArticleScrap(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=50)
    title_zh = models.CharField(max_length=50)
    author = models.CharField(max_length=30)
    content_md = models.TextField()
    content_html = models.TextField()
    tags = models.CharField(max_length=30)
    views = models.IntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

class User(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    email=models.EmailField()
    def __str__(self):
        return self.username
    class Meta:
        ordering=['username']
class ArticleScrapAdmin(admin.ModelAdmin):
    list_display=('title','created')

class UserAdmin(admin.ModelAdmin):
    list_display=('username','email')
