from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import (
    authenticate, login, logout
)
from django.contrib.auth.decorators import login_required

from web.forms.login import loginform
from web.forms.register import registerform
from web.utils.captcha import captcha
from web.utils import ip
from web.models import UserInfo


# 首页
@login_required
def index(request):
    if request.user.is_authenticated:
        title = request.user.email
    return render(request, 'web/index.html', {'title': title, 'keywords': '首页,博客,index,blog,个人网站,开发者,it'})


# 登录
def user_login(request):
    form = loginform()
    if request.method == 'POST':
        form = loginform(request.POST)
        ca = captcha(request)
        if form.is_valid() and ca.validate(form.clean_code()):
            user = authenticate(request, username=form.data['username'], password=form.data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                form.add_error('username', '用户名或密码无效')
    return render(request, 'web/account.html', {
        'isLogin': True,
        'login': form,
        'register': registerform(),
    })


# 注册
def user_register(request):
    form = registerform()
    if request.method == 'POST':
        form = registerform(request.POST)
        ca = captcha(request)
        if form.is_valid() and ca.validate(form.clean_code()):
            username = form.data['username']
            password = form.data['password']
            UserInfo.objects.create_user(username, ip.get_client_ip(request), password)
            return HttpResponseRedirect('/login/', {'form': {
                'username': username
            }})
    return render(request, 'web/account.html', {'isLogin': False, 'register': form, 'login': loginform()})


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
