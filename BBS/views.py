from django.shortcuts import render_to_response, redirect ,render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.db.models import Q
from django.template import loader, Context
from BBS.models import RegisteUserForm, MyUser, LoginUserForm, ChangeInfoForm, ArticleEditForm, Article, ArticleChangeForm, Chat, ArticleCmmtForm, ArticleCmmt
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib.auth.decorators import login_required
import http.client
import urllib.request
import json
import random
from django.core.exceptions import ValidationError
import django.contrib.staticfiles
from django.http import HttpResponse
import os
os.environ.update({"DJANGO_SETTINGS_MODULE": "config.settings"})

from django.http import HttpResponse
host = "smssh1.253.com"
#端口号
port = 80
#版本号
version = "v1.1"
#查账户信息的URI
balance_get_uri = "/msg/balance/json"
#智能匹配模版短信接口的URI
sms_send_uri = "/msg/send/json"
#创蓝账号
account  = "N7267512"
#创蓝密码
password = "jOwBRyJa4t0d48"

def send_sms(text, phone):
    params = {'account': account, 'password' : password, 'msg': urllib.parse.quote(text), 'phone':phone, 'report' : 'false'}
    params=json.dumps(params)

    headers = {"Content-type": "application/json"}
    conn = http.client.HTTPConnection(host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

def Login(request):
    if request.method == 'POST':
        print('post')
        logout(request)
        try:
             form = LoginUserForm(request.POST)
             if form.is_valid():
                 username1=form.cleaned_data['user_id']
                 password1 = form.cleaned_data['password']
                 print('username='+username1)
                 print('password='+password1)
                 user1 = authenticate(password=password1, username=username1)
                 if user1 is not None:
                     print('not None')
                     login(request, user1)
                     return redirect('/BBS/home',username="nini")
                 else:
                     error1="密码错误"
                     print(error1)
                     return render_to_response('login.html',{'error1':error1})
        except Exception as e:
            print('发生Excaption')
            return render_to_response('login.html')
    else:
        try:
            notice = request.GET.get('notice')
            if notice is not None:
                return render_to_response('login.html',{'notice':notice})
            else:
                return render_to_response('login.html')
        except Exception as e:
            notice =' '
            return render_to_response('login.html',{'notice':notice})
def registe(request):
    if  request.method == 'POST':
        try:
             uf = RegisteUserForm(request.POST)
        except Exception as e:
            print(e)
            error="注册失败，请重试"
            return render_to_response('registe.html', {'errors':error})
        if uf.is_valid():
            print(uf.cleaned_data['user_id'])
            if uf.cleaned_data['password1'] == uf.cleaned_data['password2']:
                users = User.objects.all()
                error1='用户已存在'
                for us in users:
                    if us.username==uf.cleaned_data['user_id']:
                        return render_to_response('registe.html',{'error1': error1})
                newer= User.objects.create_user(username=uf.cleaned_data['user_id'],password=uf.cleaned_data['password1'])

                myuser = MyUser(user=newer)
                myuser.save()
                notice="注册成功，"
               # return render(request,'login.html', {'notice': notice})
                return redirect('/BBS/login/?notice=注册成功，')
            else:
                error2="密码不一致"
                return render_to_response('registe.html',{'error2': error2})
        else:
            return render_to_response('registe.html')
    elif request.method=='POST1':
        print('hello post1')
        return render_to_response('registe.html')
    else:
         form = RegisteUserForm()
         print('GET')
         return render_to_response('registe.html',{'form':form})



def registecode(request):
    global randstr
    if  request.method == 'POST':
        try:
             code = request.POST.get("code")
             print('code:'+code)
             phone =  request.POST.get("phone")
             if  not code.strip() :
                 print('code is none')
                 rand=random.randint(1000,9999)
                 randstr = str(rand)
                 print('验证码：'+randstr)
                 text = "【253云通讯】您的验证码是"+randstr
                 send_sms(text, phone)
                 return render_to_response('registcode.html', {'phone':phone})
             else:
                 print('code is not  none')
                 users = User.objects.all()
                 error1='用户已存在'
                 for us in users:
                     if us.username==phone:
                         return render_to_response('registcode.html',{'error1': error1})

                 if code!=randstr:
                     error1='验证码错误'
                     return render_to_response('registcode.html',{'error1': error1})
                 newer= User.objects.create_user(username=phone,password=randstr)
                 myuser = MyUser(user=newer)
                 myuser.save()
                 notice="注册成功，"
                 # return render(request,'login.html', {'notice': notice})
                 return redirect('/BBS/login/?notice=注册成功，')

        except Exception as e:
            print(e)
            error="注册失败，请重试"
            return render_to_response('registcode.html', {'errors':error})
    else:
         print('GET')
         return render_to_response('registcode.html')

@login_required()
def home(request):
    username1=str(request.user)
    print('user:'+username1)
    user = User.objects.get(username=username1)
    myuser = MyUser.objects.get(user=user)
    try:

        photopath = str(myuser.photo)
        path=photopath[3:]
        print('path:'+path)

        #if request.method=='POST':
        keyword = request.GET.get("keyword")
        print('home POST:'+str(keyword))
        articles =[]
        print('home GET1:')
        if  keyword is not None:
            print('home GET2')
            articles1 = Article.objects.filter(name = str(keyword))
            print('home GET3')
            if len(articles1)==0:
                print('无结果')
                return render_to_response('home.html',{'userName':username1, 'photo':path})
            print('len:'+str(len(articles)))
            for article in articles1:
                print('home GET4')
                print('article_name:'+article.name)
                print('article_id:'+str(article.id))

                myuser = MyUser.objects.get(id = article.user_id)
                user1 = User.objects.get(id = myuser.user_id)
                name = user1.username
                print('author_name:'+str(name))

                user_id = MyUser.objects.get(id = int(article.user_id))
                receiver_id = user_id.user_id

                list={'id':article.id, 'article_info':article.article_info,'article_author_name':str(name), 'article_time':article.article_time,'article_date':article.article_date,'name':article.name,'receiver':str(receiver_id)}
                print('receiver_id:'+str(receiver_id))
                articles.append(list)
            print('lists:')
            return render_to_response('home.html',{'userName':username1, 'photo':path,'articles':articles})

        for article in Article.objects.all().order_by('-article_time', '-article_date'):
            print('article_name:'+article.name)
            print('article_id:'+str(article.id))

            myuser = MyUser.objects.get(id = article.user_id)
            user1 = User.objects.get(id = myuser.user_id)
            name = user1.username
            print('author_name:'+str(name))

            user_id = MyUser.objects.get(id = int(article.user_id))
            receiver_id = user_id.user_id

            list={'id':article.id, 'article_info':article.article_info,'article_author_name':str(name), 'article_time':article.article_time,'article_date':article.article_date,'name':article.name,'receiver':str(receiver_id)}
            print('receiver_id:'+str(receiver_id))
            articles.append(list)
        print('lists:')
        return render_to_response('home.html',{'userName':username1, 'photo':path,'articles':articles})
    except Exception as e:
        print('发生异常或者无照片')
        return render_to_response('home.html',{'userName':username1})

@login_required
def Logout(request):
    logout(request)
    return redirect("/BBS/login/")

@login_required
def Changeinfo(request):
    if  request.method == 'POST':
        print('POST1')
        try:
             form = ChangeInfoForm(request.POST, request._files)
             username1=str(request.user)
             print('POST2 user:'+username1)
             if form.is_valid():

                 u = User.objects.get(username=username1)
                 u.set_password(form.cleaned_data['password'])
                 u.save()

                 user=User.objects.get(username=username1)
                 print('user2: ')
                 user.email=form.cleaned_data['email']
                 user.save()
                 myuser = MyUser.objects.get(user=user)
                 print('user3: ')
                 myuser.age=form.cleaned_data['age']
                 myuser.name=form.cleaned_data['name']
                 myuser.phone=form.cleaned_data['phone']
                 myuser.sex = form.cleaned_data['sex']

                 myuser.photo = form.cleaned_data['photo']
                 print(myuser.photo.name)
                 myuser.type=0
                 myuser.save()
                 print('user3: ')
                 print('保存成功')
                #,'photo':form.cleaned_data['photo']
                 photopath="/static/upload/"+str(form.cleaned_data['photo'])
                 return render_to_response('changeinfo.html',{'username':username1,'password':form.cleaned_data['password'], 'name': form.cleaned_data['name'],  'age':form.cleaned_data['age'], 'sex':form.cleaned_data['sex'], 'phone':form.cleaned_data['phone'],'email':form.cleaned_data['email'],'photo':photopath })
             else:
                 print('form无效')
                 return render_to_response('error.html')
        except Exception as e:
            print(e)
            error="注册失败，请重试"
            print(error)
            return render_to_response('changeinfo.html')
    else:
        print('GET成功')
        username1=str(request.user)
        print('user:'+username1)
        user = User.objects.get(username=username1)
        myuser = MyUser.objects.get(user=user)
        print('password:'+user.password)
        try:
            photopath = str(myuser.photo)
            path=photopath[3:]
            print('path:'+path)
            return render_to_response('changeinfo.html',{'username':username1, 'name':myuser.name,  'age':myuser.age, 'sex':myuser.sex, 'phone':myuser.phone,'email':user.email,'photo':path})
        except Exception as e:
            print('无照片')
            return render_to_response('changeinfo.html',{'username':username1, 'name':myuser.name,  'age':myuser.age, 'sex':myuser.sex, 'phone':myuser.phone,'email':user.email})
@login_required()
def ArticleEdit(request):
    if  request.method == 'POST':
        try:

            username1=str(request.user)
            uf = ArticleEditForm(request.POST)
            if uf.is_valid():
                print('uf：')
                user1 = User.objects.get(username = username1)
                Article.objects.create(name = uf.cleaned_data['name'],article_info = uf.cleaned_data['article_info'], user = MyUser.objects.get(user = user1))
                tip='文章发布成功,请去首页查看'
                print(tip)
                return render_to_response('articleedit.html',{'name': uf.cleaned_data['name'], 'article_info': uf.cleaned_data['article_info'], 'tips': tip})

        except Exception as e:
            print(e)
            error="文章添加失败1"
            print(error)
            return render_to_response('articleedit.html',{'tips':error})
    else:
         print('GET')
         username1=str(request.user)
         print('user:'+username1)
         user = User.objects.get(username=username1)
         myuser = MyUser.objects.get(user=user)
         print('password:'+user.password)
         try:
             photopath = str(myuser.photo)
             path=photopath[3:]
             print('path:'+path)
             return render_to_response('articleedit.html',{'userName':username1,'photo':path})
         except Exception as e:
             print('无照片')
             return render_to_response('articleedit.html',{'userName':username1})

@login_required()
def ArticleChange(request):
    if request.method=='POST':
        try:
            uf = ArticleChangeForm(request.POST)
            if uf.is_valid():
                print('uf:')
                id = uf.cleaned_data['id']
                print('id:'+id)
                print('name:'+uf.cleaned_data['name'])
                print('article_info:'+uf.cleaned_data['article_info'])

                Article.objects.filter(id = int(id)).update(name = uf.cleaned_data['name'],article_info = uf.cleaned_data['article_info'])
                tip='文章修改成功'
                print(tip)
                article = Article.objects.get(id=int(id))
                return render_to_response('articlechange.html',{'nid':str(id),'article':article,'tips':tip})
            else:
                error = 'uf error'
                print(error)
                return render_to_response('articlechange.html')
        except Exception as e:
            print(e)
            error="文章修改失败1"
            print(error)
            return render_to_response('articlechange.html',{'tips':error})
    else:
         try:
             print('有参数')
             print('GET:article change')
             nid = request.GET.get('nid')
             article = Article.objects.get(id=nid)

             username1=str(request.user)
             print('user:'+username1)
             user = User.objects.get(username=username1)
             myuser = MyUser.objects.get(user=user)

             return render_to_response('articlechange.html',{ 'article':article,'nid':str(nid),'userName':username1})
         except Exception as e:
             print('无参数,或者没有照片')
             return render_to_response('articlechange.html',{'userName':username1})
@login_required()
def MyArticals(request):
    username1=str(request.user)
    user1 = User.objects.get(username = username1)
    user = MyUser.objects.get(user = user1)
    articles = Article.objects.filter(user = user)
    print('MyArticals:')
    print(articles)
    articlenum = articles.__len__()
    print('num:'+str(articlenum))
    try:
        photopath = str(user.photo)
        path=photopath[3:]
        print('path:'+path)
        return render_to_response('myarticles.html',{'articles':articles,'articlenum':str(articlenum),'userName':username1,'photo':path})
    except Exception as e:
        print('无照片')
        return  render_to_response('myarticles.html',{'articles':articles,'articlenum':str(articlenum)})

def del_article(request):
        nid = request.GET.get('nid')
        Article.objects.filter(id=nid).delete()
        return redirect('/BBS/myarticles.html')

@login_required()
def MyArticalCmmt(request):
    username1=str(request.user)
    user1 = User.objects.get(username = username1)
    user = MyUser.objects.get(user = user1)
    articlecmmts = ArticleCmmt.objects.filter(user_id = user1).order_by('-time')
    lists=[]
    for articlecmmt in articlecmmts:
        article = Article.objects.get(id = articlecmmt.article_id)
        articleuser =User.objects.get(id = articlecmmt.user_id_id)
        list = {'articlename':article.name,'articleusername':articleuser.username,'article_time':article.article_date,'info':articlecmmt.cmmt_info,'time':articlecmmt.time,'id':articlecmmt.id}
        print('article_time:'+str(article.article_date))
        lists.append(list)
    print('lists:')

    articlecmmtnum = articlecmmts.__len__()
    print('srticlecmmt num:'+str(articlecmmtnum))

    try:
        photopath = str(user.photo)
        path=photopath[3:]
        print('path:'+path)
        return render_to_response('myarticlecmmts.html',{'articlecmmts':lists,'articlenum':str(articlecmmtnum),'userName':username1,'photo':path})
    except Exception as e:
        print('无照片')
        return  render_to_response('myarticlecmmts.html',{'articlecmmts':lists,'articlenum':str(articlecmmtnum),'userName':username1})

def del_articlecmmt(request):
        nid = request.GET.get('nid')
        ArticleCmmt.objects.filter(id=nid).delete()
        return redirect('/BBS/myarticlecmmts.html')
@login_required()
def chat(request):
    user = str(request.user)
    userid = User.objects.get(username = user).id
    print('index1:')
    print('index2:')
    receiver_id = request.GET.get('receiver')
    print('receiver_id:'+str(receiver_id))
    chats = Chat.objects.filter( Q(sender_id = int(userid), receiver = int(receiver_id))| Q(sender_id = int(receiver_id), receiver = int(userid)))

    receiveusername = User.objects.get(id = int(receiver_id)).username

    return render(request, 'chatroom.html', {'chats': chats,'receiver':str(receiver_id),'userName':user,'receiveusername':receiveusername})

@csrf_exempt
@login_required()
def post(request):
    user = str(request.user)
    userid = User.objects.get(username = user).id
    if request.method == 'POST':
        post_type = request.POST.get('post_type')
        receiver = request.POST.get('receiver')
        if post_type == 'send_chat':
            print('send_chat:')
            print('receiver:'+str(receiver))
            new_chat = Chat.objects.create(
                content = request.POST.get('content'),
                sender = request.user,
                receiver = receiver,
            )
            new_chat.save()
            return HttpResponse()
        elif post_type == 'get_chat':
            print('get_chat:')
            last_chat_id = request.POST.get('last_chat_id')
            if last_chat_id is None:
                last_chat_id=1
            print('last_chat_id:'+str(last_chat_id))
            print('userid:'+str(userid))
            print('receiver:'+str(receiver))
            chats = Chat.objects.filter(Q(id__gt = last_chat_id, sender_id = receiver, receiver = int(userid))| Q(id__gt = last_chat_id,sender_id = int(userid), receiver = receiver))
            #chats = Chat.objects.filter(id__gt = last_chat_id)
            for chat in chats:
                print('收到：id'+str(chat.id)+'receiver：'+str(chat.receiver)+'sender：'+str(chat.sender)+'info:'+chat.content)
           # chats = Chat.objects.filter(id__gt = last_chat_id, receiver = int(userid))
            return render(request, 'chat_list.html', {'chats': chats,'userName':user})
    else:
        return  HttpResponse("404")
@login_required()
def SingleArticle(request):
    user = str(request.user)
    userid = User.objects.get(username = user).id
    print('userid:'+str(userid))
    if request.method=='POST':
        try:
            uf = ArticleCmmtForm(request.POST)
            if uf.is_valid():
                print('uf:')
                articleid = uf.cleaned_data['articleid']
                print('articleid:'+str(articleid))
                cmmt_info = uf.cleaned_data['cmmt_info']
                print('cmmt_info:'+cmmt_info)

                ArticleCmmt.objects.create(article_id = articleid, cmmt_info = cmmt_info, user_id = request.user )

                tip='评论添加成功'
                print(tip)

                articlecmmts = ArticleCmmt.objects.filter(article_id = int(articleid))
                lists=[]
                for articlecmmt in articlecmmts:
                    print('articlecmmt1:')
                    user1 = User.objects.get(id = int(articlecmmt.user_id_id))
                    print('user1:username:'+user1.username)
                    lt = {'cmmt_info':articlecmmt.cmmt_info, 'time':articlecmmt.time, 'username':user1.username}
                    lists.append(lt)

                article = Article.objects.get(id=int(articleid))
                return render_to_response('singlearticle.html',{ 'article':article,'nid':str(articleid),'articlecmmts':lists})
            else:
                error = 'uf error'
                print(error)
                return render_to_response('articlechange.html')
        except Exception as e:
            print(e)
            error="文章修改失败1"
            print(error)
            return render_to_response('articlechange.html',{'tips':error})
    else:
         try:
             print('Single article有参数')
             print('GET:Single article ')
             nid = request.GET.get('nid')
             article = Article.objects.get(id=nid)
             print('nid:'+str(nid))

             articlecmmts = ArticleCmmt.objects.filter(article_id = int(nid))

             lists=[]
             for articlecmmt in articlecmmts:
                 print('articlecmmt1:')
                 user1 = User.objects.get(id = int(articlecmmt.user_id_id))
                 print('user1:username:'+user1.username)
                 lt = {'cmmt_info':articlecmmt.cmmt_info, 'time':articlecmmt.time, 'username':user1.username}
                 lists.append(lt)
             print('list:')
             userr = User.objects.get(username=user)
             myuser = MyUser.objects.get(user=userr)
             photopath = str(myuser.photo)
             path=photopath[3:]
             print('path:'+path)

             return render_to_response('singlearticle.html',{ 'article':article,'nid':str(nid),'articlecmmts':lists,'userName':user,'photo':path})
         except Exception as e:
             print('无参数,或者无照片')
             return render_to_response('singlearticle.html',{'userName':user})
randstr = 'helo'

def index(request):
    return render_to_response('index.html')