#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-9-23 下午2:08
# @Author  : whl
# @File    : UserAuthenticate.py
# @Software: PyCharm

from web.models import UserInfo


class UserAuthenticate:
    """自定义用户授权"""

    def authenticate(self, request, username=None, password=None):
        try:
            return UserInfo.objects.get(email=username, password=password)
        except UserInfo.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserInfo.objects.get(pk=user_id)
        except UserInfo.DoesNotExist:
            return None
