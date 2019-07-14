import os
import time
import base64
import logging
import random

from django.contrib.auth import (
    authenticate, login, logout
)
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.conf import settings
from django.db.models import F

from web.cache import CacheArticles

from web.forms import *
from web.models import UserInfo, UploadFile, Article, Category
from web.utils import ip, email
from web.utils.captcha import captcha

logger = logging.getLogger(__name__)

# 首页
def index(request, user_id=0, pager=1, size=10):
    user = None
    pager = (1, pager)[pager > 0]
    if user_id and user_id > 0:
        user = UserInfo.objects.first(id=user_id)
        articles = Article.objects.filter(create_user_id=user_id, is_deleted=False).order_by('-topping',
                                                                                             '-create_time',
                                                                                             'id')[(pager - 1) * size:pager * size]
        count = Article.objects.filter(
            create_user_id=user_id, is_deleted=False).count()
    else:
        articles = Article.objects.filter(is_deleted=False).order_by(
            '-topping', '-create_time', 'id')[(pager - 1) * size:pager * size]
        count = Article.objects.filter(is_deleted=False).count()
    items = []
    categories = Category.objects.filter(
        is_deleted=False).order_by('level', 'sort', 'create_time')
    authors = Article.objects.values(
        'create_user__id', 'create_user__username', 'create_user__email').distinct()
    for item in articles:
        categoryids = item.category_ids.split(',')
        names = [category.name for category in categories if str(category.id) in categoryids][:5]
        hits = CacheArticles.get_reading(item.id)
        if hits == 0:
            CacheArticles.reading(item.id, item.hits)
            hits = item.hits
        items.append({
            'id': item.id,
            'title': item.title,
            'subject': item.subject,
            'cover': item.cover,
            'tags': [],
            'categories': names,
            'hits': hits,
            'create_time': item.create_time,
            'create_user_id': item.create_user.id,
            'create_user_name': (item.create_user.username, item.create_user.email)[item.create_user.username == ''],
            'update_time': item.update_time,
            'user_avatar': item.create_user.avatar
        })
    total_pager = (int(count / size) + 1, int(count / size))[int(count % size) == 0]
    if total_pager - pager >= size:
        pagers = range(pager, pager + size)
    else:
        pagers = range((1,total_pager - size + 1)[total_pager - size > 0], total_pager + 1)
    return render(request, 'web/index.html', {'articles': items,
                                              'categories': categories[:10],
                                              'authors': authors[:10],
                                              'user': (user, request.user)[user is None],
                                              'count': count,
                                              'pager': pager,
                                              'pagers': pagers,
                                              'pager_url_prefix': ('/index/u%d' % user_id, '/index')[user is None],
                                              'total_pager': total_pager,
                                              'number': random.randint(1, 5)
                                              })


# 博客编辑
@login_required
def article(request, article_id=0):
    form = ArticleForm()
    model = None
    categories = Category.objects.filter(is_deleted=False).order_by('level', 'sort', 'create_time') \
        .values('id', 'name', 'spell')
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            category_ids = ','.join(str(i['id'])
                                    for i in form.get_categories().values('id'))
            model = Article(title=form.get_title(), subject=form.get_subject(), cover=form.get_cover(),
                            content=form.get_content(), category_ids=category_ids, topping=form.get_topping(),
                            tag_ids='', hits=0, score=0)
            if article_id > 0:
                model.id = article_id
            Article.objects.save_new(model, request.user)
            CacheArticles.delete(model.id)
    elif article_id > 0:
        model = Article.objects.first(id=article_id)
    if model:
        form = ArticleForm({
            'title': model.title,
            'subject': model.subject,
            'content': model.content,
            'cover': model.cover,
            'topping': model.topping
        })
        category_ids = model.category_ids.split(',')
        for category in categories:
            if str(category['id']) in category_ids:
                category['checked'] = 'checked'
        if request.method == 'POST' and model.id > 0:
            return HttpResponseRedirect('/reading/%d/' % model.id, {
                'article': form,
                'categories': categories
            })
    return render(request, 'web/article.html', {
        'article': form,
        'categories': categories
    })


# 上传
@login_required
def upload(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.clean_file()
            name = '%s%s%s' % (int(time.time()), request.user.id,
                               os.path.splitext(file.name)[-1])
            file.name = name
            model = UploadFile(create_user=request.user, name=file.name, type=file.content_type,
                               size=file.size, file=file)
            model.save()
            return JsonResponse({'success': 1, 'url': model.file.url, 'message': '上传成功!'})
    return JsonResponse({'success': 0, 'message': '上传失败!'})


# 阅读文章
def reading(request, article_id):
    data = None
    if article_id and article_id > 0:
        model = None
        data = CacheArticles.get(article_id)
        if data is None:
            model = Article.objects.first(id=article_id)
            if model:
                data = {
                    'id': model.id,
                    'title': model.title,
                    'subject': model.subject,
                    'content': model.content,
                    'cover': model.cover,
                    'category_ids': model.category_ids,
                    'tag_ids': model.tag_ids,
                    'create_user_id': model.create_user.id,
                    'create_user_email': (model.create_user.username, model.create_user.email)[model.create_user.username == ''],
                    'create_time': model.create_time.strftime('%Y/%m/%d %H:%M')
                }
                CacheArticles.set(article_id, data)
        data['isowner'] = request.user.is_authenticated and data['create_user_id'] is request.user.id
        if request.user and request.user.is_authenticated:
            ip_str = ip.get_client_ip(request)
            if CacheArticles.get_reading_key(article_id, request.user.id ,ip_str) == 0:
                Article.objects.filter(id=article_id).update(hits=F('hits') + 1)
                CacheArticles.reading(article_id, 1)
                CacheArticles.set_reading_key(article_id, request.user.id, ip_str)
    return render(request, 'web/reading.html', {
        'article': data,
        'hints': [
            '请简单粗暴地爱我。',
            '此处应有打赏',
             '拿钱去买猫粮，楼下的流浪猫在等我('')ﾉ',
              '请赏我点铜板买狗粮自己吃，谢谢！'
        ]
    })


# 删除文章
@login_required
def delete_article(request, article_id):
    message = '你还有没有登录！'
    if request.user and request.user.is_authenticated:
        model = Article.objects.first(id=article_id)
        if model and model.create_user.id == request.user.id:
            CacheArticles.delete(article_id)
            model.is_deleted = True
            Article.objects.save_new(model, request.user)
            return JsonResponse({'isSuccess': True, 'message': '删除成功！'})
        message = '你无权删除该文章！'
    return JsonResponse({'isSuccess': False, 'message': message})


# 登录
def user_login(request):
    form = LoginFrom()
    if request.method == 'POST':
        form = LoginFrom(request.POST)
        ca = captcha(request)
        if form.is_valid() and ca.validate(form.clean_code()):
            user = authenticate(
                request, username=form.data['username'], password=form.data['password'])
            if user:
                if user.authorized:
                    login(request, user)
                    return HttpResponseRedirect(request.GET.get('next', '/'))
                else:
                    form.add_error('username', '账户邮箱未验证，请查阅邮件完成验证后登录')
            else:
                form.add_error('username', '用户名或密码无效')
    return render(request, 'web/account.html', {
        'is_login': 'is-active',
        'next': request.GET.get('next', '/'),
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
            UserInfo.objects.create_user(
                username, ip.get_client_ip(request), password)
            # 发送电子邮件，进行身份验证
            host = '%s://%s' % (request.scheme, request.get_host())
            token = signing.dumps({'email': username, 'timestamp': int(time.time())},
                                  base64.b64encode(settings.SECRET_KEY.encode('ascii')))
            email.send_email_confirm(host, username, token)
            logger.info('用户(%s)注册确认邮件已发送!\nToken:%s' % (username, token))

            return HttpResponseRedirect('/login/', {'form': {
                'username': username
            }})
    return render(request, 'web/account.html', {
        'is_register': 'is-active',
        'next': request.GET.get('next', '/'),
        'register': form,
        'login': LoginFrom()
    })


# 用户中心
@login_required
def user_info(request):
    form = UserEditor()
    if request.user and request.user.is_authenticated:
        if request.method == 'POST':
            form = UserEditor(request.POST)
            form.id = request.user.id
            avatar = FileForm(request.POST, request.FILES)
            if form.is_valid():
                model = request.user
                model.username = form.clean_username()
                model.sex = form.clean_sex()
                model.birthday = form.clean_birthday()
                model.introduce = form.clean_introduction()
                model.update_time = timezone.now()
                if avatar.is_valid():
                    file = avatar.clean_file()
                    name = '%s%s%s' % (
                        int(time.time()), request.user.id, os.path.splitext(file.name)[-1])
                    file.name = name
                    avatar_model = UploadFile(create_user=request.user, name=file.name, type=file.content_type,
                                              size=file.size, file=file)
                    avatar_model.save()
                    model.avatar = avatar_model.file.url
                model.save()
                return HttpResponseRedirect('/')
        else:
            user = request.user
            if not user.birthday:
                user.birthday = timezone.now().replace(year=timezone.now().year - 23)
            form = UserEditor({
                'username': user.username,
                'avatar': user.avatar,
                'sex': user.sex,
                'birthday': user.birthday,
                'introduction': user.introduce
            })
    return render(request, 'web/userinfo.html', {
        'user': form
    })


# 用户注册验证确认
def user_confirm(request, token):
    username = None
    success = False
    if token:
        second = settings.EMAIL_CONFIRM_DAYS * 24 * 60 * 60
        try:
            data = signing.loads(s=token, key=base64.b64encode(
                settings.SECRET_KEY.encode('ascii')), max_age=second)
            if data:
                user = UserInfo.objects.first(email=data['email'])
                if user and user.authorized is False:
                    user.authorized = True
                    UserInfo.save(user)
                    username = user.email
                    success = True
        except signing.SignatureExpired:
            pass
        except signing.BadSignature:
            pass
    return render(request, 'web/confirm.html', {
        'success': success,
        'username': username
    })


# 关于
def about(request):
    return render(request, 'web/about.html')


# 注销
@login_required
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
