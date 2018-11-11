from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import (
    authenticate, login, logout
)
from django.contrib.auth.decorators import login_required

from web.models import UserInfo, UploadFile, Article
from web.utils.captcha import captcha
from web.utils import ip
from web.forms import *


# 首页
def index(request, user_id=0, pager=0, size=20):
    title = '欢迎来到本站'
    if request.user.is_authenticated:
        title = request.user.email
    if user_id and user_id > 0:
        articles = Article.objects.filter(create_user_id=user_id)[pager:size]
        count = Article.objects.filter(create_user_id=user_id).count()
    else:
        articles = Article.objects.all()[pager:size]
        count = Article.objects.count()
    items = []
    for item in articles:
        items.append({
            'id': item.id,
            'title': item.title,
            'subject': item.subject,
            'content': item.content,
            'cover': item.cover,
            'tags': ['Python', '高并发'],
            'categories': ['大数据'],
            'hits': 99,
            'create_time': item.create_time,
            'create_user_id': item.create_user.id,
            'create_user_name': item.create_user.email,
            'update_time': item.update_time
        })

    return render(request, 'web/index.html', {'title': title, 'keywords': '首页,博客,index,blog,个人网站,开发者,it',
                                              'articles': items,
                                              'categories': [],
                                              'count': count,
                                              'pager': pager,
                                              'total_pager': (int(count / size) + 1, int(count / size))[
                                                  int(count % size) == 0]
                                              })


# 博客编辑
@login_required
def article(request, article_id=0):
    form = ArticleForm()
    model = None
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            model = Article(title=form.get_title(), subject=form.get_subject(), cover=form.get_cover(),
                            content=form.get_content(), category_ids=form.get_category_ids(),
                            tag_ids=form.get_tag_ids(), hits=0, score=0)
            if article_id > 0:
                model.id = article_id
            Article.objects.save_new(model, request.user)
    elif article_id > 0:
        model = Article.objects.first(id=article_id)
    if model:
        form = ArticleForm({
            'title': model.title,
            'subject': model.subject,
            'content': model.content,
            'cover': model.cover,
            'category_ids': model.category_ids,
            'tag_ids': model.tag_ids
        })
        if article_id <= 0 and model.id:
            return HttpResponseRedirect('/article/%d/' % model.id, {
                'article': form
            })
    return render(request, 'web/article.html', {
        'article': form
    })


# 上传
@login_required
def upload(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.clean_file()
            model = UploadFile(create_user=request.user, name=file.name, type=file.content_type,
                               size=file.size, file=file)
            model.save()
            return JsonResponse({'uploaded': True, 'url': model.file.url});
    return JsonResponse({'uploaded': False, 'error': {'message': '请求方式错误！'}})


# 登录
def user_login(request):
    form = LoginFrom()
    if request.method == 'POST':
        form = LoginFrom(request.POST)
        ca = captcha(request)
        if form.is_valid() and ca.validate(form.clean_code()):
            user = authenticate(request, username=form.data['username'], password=form.data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                form.add_error('username', '用户名或密码无效')
    return render(request, 'web/account.html', {
        'is_login': 'is-active',
        'login': form,
        'register': RegisterForm(),
    })


# 注册
def user_register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        ca = captcha(request)
        if form.is_valid() and ca.validate(form.clean_code()):
            username = form.data['username']
            password = form.data['password']
            UserInfo.objects.create_user(username, ip.get_client_ip(request), password)
            return HttpResponseRedirect('/login/', {'form': {
                'username': username
            }})
    return render(request, 'web/account.html', {
        'is_register': 'is-active',
        'register': form,
        'login': LoginFrom()
    })


# 注销
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


# 验证码
def captcha_code(request):
    ca = captcha(request)
    ca.type = 'number'
    raw = ca.display()
    response = HttpResponse(raw, content_type='image/gif')
    return response
