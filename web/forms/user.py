# /usr/bin/env python
# ! -*- coding:utf-8 -*-

from django import forms
from web.models import UserInfo


class LoginFrom(forms.Form):
    """
    用户登录表单
    """

    username = forms.CharField(required=True, min_length=4, max_length=50, initial='',
                               error_messages={
                                   'required': '请输入用户名或邮箱',
                                   'min_length': '用户名至少4个字符',
                                   'max_length': '用户名最多50个字符'
                               })
    password = forms.CharField(required=True, min_length=8, max_length=16, initial='',
                               error_messages={
                                   'required': '请输入登录密码',
                                   'min_length': '密码最少8个字符',
                                   'max_length': '密码最多16个字符'
                               })
    code = forms.CharField(required=True, initial='', error_messages={'required': '请输入验证码'})

    def clean_username(self):
        username = self.cleaned_data['username']
        if username is None:
            raise forms.ValidationError('请输入用户名')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if password is None:
            raise forms.ValidationError('请输入密码')
        return password

    def clean_code(self):
        code = self.cleaned_data['code']
        if code is None:
            raise forms.ValidationError('请输入验证码')
        return code

    def clean(self):
        super().clean()


class RegisterForm(forms.Form):
    """
    用户注册表单
    """
    username = forms.CharField(required=True, min_length=4, max_length=50, label='', initial='',
                               error_messages={'required': '用户名不能为空'},
                               widget=forms.TextInput(attrs={'placeholder': '请输入用户名'}))
    password = forms.CharField(required=True, min_length=8, max_length=16, label='', initial='',
                               error_messages={'required': '密码不能为空'},
                               widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'}))
    re_password = forms.CharField(required=True, min_length=8, max_length=16, label='', initial='',
                                  error_messages={'required': '密码不能为空'},
                                  widget=forms.PasswordInput(attrs={'placeholder': '请再次输入密码'}))
    code = forms.CharField(required=True, label='', initial='',
                           error_messages={'required': '验证码不能为空'})

    class Meta:
        model = UserInfo
        fields = ('email', 'ip')

    def clean_username(self):
        username = self.cleaned_data['username']
        users = UserInfo.objects.filter(email=username)
        if len(users) > 0:
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        return password

    def clean_re_password(self):
        password = self.cleaned_data['password']
        repassword = self.cleaned_data['re_password']
        if password and repassword and password != repassword:
            raise forms.ValidationError('两次输入的密码不一致')
        return repassword

    def clean_code(self):
        code = self.cleaned_data['code']
        return code
