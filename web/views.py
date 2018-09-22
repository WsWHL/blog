from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from web.forms.login import loginform
from web.forms.register import registerform

from web.utils.captcha import captcha

from web.models import UserInfo


# 首页
def index(request):
    return render(request, 'web/index.html', {'keywords': '首页,博客,index,blog,个人网站,开发者,it'})


# 登录
def login(request):
    form = loginform()
    if request.method == 'POST':
        form = loginform(request.POST)
        ca = captcha(request)
        if form.is_valid() and ca.validate(form.clean_code()):
            name = form.data['username']
            return HttpResponseRedirect('/')
    return render(request, 'web/account.html', {
        'isLogin': True,
        'login': form,
        'register': registerform(),
    })


# 注册
def register(request):
    form = registerform()
    if request.method == 'POST':
        form = registerform(request.POST)
        ca = captcha(request)
        if form.is_valid() and ca.validate(form.clean_code()):
            username = form.data['username']
            password = form.data['password']
            user = UserInfo(Email=username, CheckKey='ahdksk', Password=password, IP='110.66.66.78')
            user.save()
            return HttpResponseRedirect('/login/', {'form': {
                'username': username
            }})
    return render(request, 'web/account.html', {'isLogin': False, 'register': form, 'login': loginform()})


# 验证码
def captcha_code(request):
    ca = captcha(request)
    ca.type = 'number'
    raw = ca.display()
    response = HttpResponse(raw, content_type='image/gif')
    return response
