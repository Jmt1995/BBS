from django.contrib import admin
from BBS.models import MyUser, Article, Chat

admin.site.register(MyUser)
admin.site.register(Article)
admin.site.register(Chat)
