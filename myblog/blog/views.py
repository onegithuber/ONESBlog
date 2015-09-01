#!/usr/bin/env python
# coding=utf-8
from django.core.urlresolvers import reverse
from django.shortcuts import render,render_to_response
from forms import ArticlePublishForm,RegisterForm
from models import ArticleScrap
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import qrcode
from cStringIO import StringIO
import json
from django.db.models import Q
class BaseMixin(object):
    def get_context_data(self,*args,**kwargs):
        context = super(BaseMixin,self).get_context_data(**kwargs)
        context['article_list'] = ArticleScrap.objects.all().order_by("-views")[0:10]
        img = qrcode.make(self.request.get_full_path())
        buf = StringIO()
        img.save(buf)
        image_stream = buf.getvalue()
        response = HttpResponse(image_stream, content_type="image/png")
        context['url_image'] = response
        return context

def SearchView(request):
    if request.method == 'GET':
        search = request.GET.get('search','')
        posts = ArticleScrap.objects.filter(Q(title__icontains=search)|Q(author__icontains=search)|Q(tags__icontains=search)|Q(content_html__icontains=search))
        article_list=ArticleScrap.objects.all().order_by('-views')
        paginator=Paginator(posts,10)
        page_num=request.GET.get('page')
        try:
            posts=paginator.page(page_num)
        except PageNotAnInteger:
            posts=paginator.page(1)
        except EmptyPage:
            posts=paginator.page(page.num_pages)
        return render(request,'search.html',locals())




@login_required(redirect_field_name='index/')
def index(request):
    posts=ArticleScrap.objects.all().order_by('-created')
    article_list=ArticleScrap.objects.all().order_by('-views')
    paginator=Paginator(posts,10)
    page_num=request.GET.get('page')
    try:
        posts=paginator.page(page_num)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(page.num_pages)
    return render(request,'index.html',locals())

def loginview(request):
    errors= []
    username=None
    password=None
    if request.method == 'POST' :
        if not request.POST.get('username'):
            errors.append('Please Enter username')
        else:
            username = request.POST.get('username')
        if not request.POST.get('password'):
            errors.append('Please Enter password')
        else:
            password= request.POST.get('password')
        if username is not None and password is not None :
            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect('/index')
                else:
                    errors.append('disabled username')
            else :
                    errors.append('invaild user')
    return render_to_response('login.html', {'errors': errors})

def loginoutview(request):
    logout(request)
    return HttpResponseRedirect('/index')

class ArticleEdit(FormView):
    template_name='articleedit.html'
    form_class=ArticlePublishForm
    success_url='/index/'
    def form_valid(self,form):
        form.save(self.request.user.username)
        return super(ArticleEdit, self).form_valid(form)

class ArticleDetailView(BaseMixin,DetailView):
    template_name = 'article_detail.html'
    def get_object(self, **kwargs):
        title = self.kwargs.get('title')
        image=qrcode.make(self.request.get_full_path())
        buf = StringIO()
        image.save(buf)
        image_stream = buf.getvalue()
        response = HttpResponse(image_stream, content_type="image/png")
        try:
            article = ArticleScrap.objects.get(url=title)
            article.views += 1
            article.save()
            article.tags = article.tags.split()
        except ArticleScrap.DoesNotExist:
            raise Http404("Article does not exist")
        return article



class RegisterView(FormView):
    template_name='register.html'
    form_class=RegisterForm
    success_url='/index/'
    def form_valid(self,form):
        form.save()
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        user=authenticate(username=username,password=password)
        login(self.request, user)
        return super(RegisterView,self).form_valid(form)




def url_qrcode(request):
    img = qrcode.make(request.get_full_path())

    buf = StringIO()
    img.save(buf)
    image_stream = buf.getvalue()

    response = HttpResponse(image_stream, content_type="image/png")
    response['Last-Modified'] = 'Mon, 27 Apr 2015 02:05:03 GMT'
    response['Cache-Control'] = 'max-age=31536000'
    return response

