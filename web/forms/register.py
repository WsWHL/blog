# /usr/bin/env python
# ! -*- coding:utf-8 -*-

from django import forms
from web.models import UserInfo


class registerform(forms.Form):
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

    def clean_username(self):
        username = self.cleaned_data['username']
        users = UserInfo.objects.filter(Email=username)
        if len(users) > 0:
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        return password

    def clean_re_password(self):
        repassword = self.cleaned_data['re_password']
        if repassword != self.clean_password():
            raise forms.ValidationError('两次输入的密码不一致')
        return repassword

    def clean_code(self):
        code = self.cleaned_data['code']
        return code
