#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-9-23 下午9:21
# @Author  : whl
# @File    : ip.py
# @Software: PyCharm


# 获取IP地址
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.spit(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
