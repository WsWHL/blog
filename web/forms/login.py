# /usr/bin/env python
# ! -*- coding:utf-8 -*-

from django import forms
from web.models import UserInfo


class loginform(forms.Form):
    """
    用户登录表单
    """

    username = forms.CharField(required=True, min_length=4, max_length=50, initial='')
    password = forms.CharField(required=True, min_length=8, max_length=16, initial='')
    code = forms.CharField(required=True, initial='')

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
        users = UserInfo.objects.filter(Email=self.data['username'], Password=self.data['password'])
        if len(users) == 0:
            self.add_error('username', '用户名或密码无效')
