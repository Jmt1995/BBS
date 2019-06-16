from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
import django.contrib.staticfiles
import os
os.environ.update({"DJANGO_SETTINGS_MODULE": "BBSPro.settings"})

class RegisteUserForm(forms.Form):
    user_id = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
class ChangeInfoForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField()
    name = forms.CharField()

    sex = forms.CharField()
    age = forms.IntegerField()
    phone = forms.CharField()
    email = forms.EmailField()
    photo = forms.FileField()

class LoginUserForm(forms.Form):
    user_id = forms.CharField()
    password = forms.CharField()
class ArticleEditForm(forms.Form):
    name = forms.CharField()
    article_info = forms.CharField()

class ArticleChangeForm(forms.Form):
    id = forms.CharField()
    name = forms.CharField()
    article_info = forms.CharField()

class ArticleCmmtForm(forms.Form):
    cmmt_info = forms.CharField(max_length=200)
    articleid = forms.IntegerField()

class MyUser(models.Model):
    user=models.OneToOneField(User)
    name = models.CharField(max_length=20,null=True)
    age = models.IntegerField(null=True)
    sex = models.CharField(max_length=20,null=True)
    phone = models.CharField(max_length=20,null=True)
    photo = models.FileField(upload_to='./BBS/static/upload/',null=True)
    type = models.IntegerField()
    def __str__(self):
        return  str(self.user)

class Article(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(MyUser)
    article_info = models.CharField(max_length=500)
    article_date = models.TimeField(auto_now_add=True)
    article_time = models.DateField(auto_now_add=True)
    def __str__(self):
        return  self.name

class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='has_chats')
    receiver = models.IntegerField()
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return u'%s' % self.content

class ArticleCmmt(models.Model):
    article = models.ForeignKey(Article)
    cmmt_info = models.CharField(max_length=200)
    user_id = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  self.cmmt_info