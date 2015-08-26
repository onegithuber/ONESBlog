from django.contrib import admin
from .models import ArticleScrap,ArticleScrapAdmin,User,UserAdmin

admin.site.register(ArticleScrap,ArticleScrapAdmin)
admin.site.register(User,UserAdmin)
