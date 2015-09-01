from django.conf.urls import url,include
from views import ArticleEdit, ArticleDetailView,RegisterView
urlpatterns=[
        url(r'^$','blog.views.index',name='index'),
        url(r'^article/publish/$',ArticleEdit.as_view(),name='ArticleEdit'),
        url(r'^article/(?P<title>\S+)$',ArticleDetailView.as_view(),name='ArticleDetail'),
        url(r'^register/$',RegisterView.as_view(),name='register'),
        url(r'^login/$','blog.views.loginview',name='login'),
        url(r'^loginout/$','blog.views.loginoutview',name='loginoutview'),
        url(r'^url_image/','blog.views.url_qrcode'),
        url(r'^search/','blog.views.SearchView'),
]
