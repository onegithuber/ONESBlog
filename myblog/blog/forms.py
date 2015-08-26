#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import datetime
import re
import markdown

from django import forms
from django.contrib.auth.models import User
from models import ArticleScrap
import sys
reload(sys)

sys.setdefaultencoding('utf-8')
class ArticlePublishForm(forms.Form):

    title = forms.CharField(
        label=u'文章标题',
        max_length=50,
        widget=forms.TextInput(attrs={'class': '', 'placeholder': u'文章标题，记得在标题末尾添加".html"'}),
        )

    content = forms.CharField(
        label=u'内容',
        min_length=5,
        widget=forms.Textarea( attrs={'class': '','style':'background-color:#ffffff'}),
        )

    tags = forms.CharField(
        label=u'标签',
        max_length=30,
        widget=forms.TextInput(attrs={'class': '', 'placeholder': u'文章标签，以空格进行分割'}),
        )

    def save(self, username):
        cd = self.cleaned_data
        title = cd['title']
        title_zh = title
        now = datetime.datetime.now()
        content_md = cd['content']
        content_html = markdown.markdown(cd['content'])
        re_title = '<h\d>(.+)</h\d>'
        data = content_html.split('\n')
        for line in data:
            title_info = re.findall(re_title, line)
            if title_info:
                title_zh = title_info[0]
                break
        url = '%s' % (title)
        tags = cd['tags']
        article = ArticleScrap(
            url=md5(url),
            title=title,
            title_zh=title_zh,
            author=username,
            content_md=content_md,
            content_html=content_html,
            tags=tags,
            views=0,
            created=now,
            updated=now)
        article.save()


class RegisterForm(forms.Form):
    username=forms.CharField(
                             max_length=20,
                             label=u'用户名',
                             initial='',
                             widget=forms.TextInput(attrs={'class': 'form-control'}),
                             )
    password=forms.CharField(
                             initial='',
                             min_length=6,
                             max_length=20,
                             label=u'密码',
                             widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                             )
    email=forms.EmailField(
                           label=u'电子邮件',
                           max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           initial='',
                           )

    def save(self):
        cd=self.cleaned_data
        username=cd['username']
        password=cd['password']
        email=cd['email']
        user = User.objects.create_user(username, email, password)
        user.save()



class LoginForm(forms.Form):
    username=forms.CharField(
                             label='username',
                             max_length=20,
                             )
    password=forms.CharField(
                             label='password',
                             max_length=20,
                             widget=forms.PasswordInput(),
                             )






def md5(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()
