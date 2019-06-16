
from django.conf.urls import url
from django.contrib import admin
from  BBS.views import Login, registe,home,Logout, Changeinfo, ArticleEdit, MyArticals, del_article, ArticleChange,chat, post, SingleArticle,registecode, MyArticalCmmt,index,del_articlecmmt
import django.contrib.staticfiles
from django import views
from django.contrib.auth.views import login
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^BBS/login/', Login ),
    url(r'^BBS/login/$', django.contrib.auth.views.login ),
    url(r'^BBS/registe/', registe ),
    url(r'^BBS/registecode/', registecode ),

    url(r'^BBS/home/',home),
    url(r'^BBS/logout',Logout),
    url(r'^BBS/changeinfo',Changeinfo),
    url(r'^BBS/articleedit',ArticleEdit),
    url(r'^BBS/myarticles',MyArticals),
    url(r'^BBS/myarticlecmmts',MyArticalCmmt),
    url(r'^BBS/articlechange',ArticleChange),
    url(r'^BBS/del_article.html$',del_article),
    url(r'^BBS/del_articlecmmts.html$',del_articlecmmt),
    url(r'^BBS/chat', chat),
    url(r'^BBS/post/$', post),
    url(r'^BBS/singlearticle',SingleArticle),
    url(r'^BBS/index/', index ),


    url(r'^static/(?P<path>.*)$',django.views.static.serve,{'document_root':settings.STATIC_ROOT})
]
