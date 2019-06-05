#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-9-16 下午1:55
# @Author  : whl
# @File    : captcha.py
# @Software: PyCharm

import os
import random
from math import ceil
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings


class captcha(object):
    """验证码类"""

    def __init__(self, request):
        self.django_request = request
        self.session_key = request.session.session_key

        self.words = []
        self.img_width = 150
        self.img_height = 50
        self.type = 'number'

    def _get_random_color(self, begin=0, end=255):
        """随机颜色"""
        return (random.randint(begin, end), random.randint(begin, end), random.randint(begin, end))

    def _get_font_size(self):
        """将图片高度的80%作为字体大小"""
        s1 = int(self.img_height * 0.3)
        s2 = int(self.img_width / len(self.code))
        return int(min((s1, s2)) + max((s1, s2)) * 0.3)

    def _get_words(self):
        """扩充单词列表"""
        if self.words:
            return set(self.words)

        file_path = os.path.join(current_path, 'words.list')
        with open(file_path, 'r') as f:
            return set([line.replace('\n', '') for line in f.readlines()])
        return None

    def _set_answer(self, answer):
        """设置答案"""
        self.django_request.session[self.session_key] = int(answer)

    def _generate_code(self):
        """生成验证码及答案"""

        def number():
            m, n = 1, 50
            x = random.randrange(m, n)
            y = random.randrange(m, n)

            r = random.randrange(0, 2)
            if r == 0:
                if x < y:
                    x, y = y, x
                code = '%s-%s=?' % (x, y)
                z = x - y
            else:
                code = '%s+%s=?' % (x, y)
                z = x + y
            # elif r == 2:
            #     code = '%s*%s=?' % (x, y)
            #     z = x * y
            # else:
            #     code = '%s/%s=?' % (x, y)
            #     z = x / y
            self._set_answer(z)
            return code

        fun = eval(self.type.lower())
        return fun()

    def display(self):
        """把生成的验证码图片改成数据流返回"""
        self.font_colors = ['black', 'darkblue', 'darkred']
        self.background = self._get_random_color(230)
        self.font_path = os.path.join(settings.STATIC_ROOT, 'fonts', 'FiraCode-Retina.ttf')

        # 生成的验证码只做一次验证
        self.django_request.session[self.session_key] = ''

        im = Image.new('RGB', (self.img_width, self.img_height), self.background)
        self.code = self._generate_code()
        self.font_size = self._get_font_size()

        # 实例化一个绘图
        draw = ImageDraw.Draw(im)
        # 在画布绘图写验证码
        if self.type == 'word':
            c = int(8 / len(self.code) * 3) or 3
        else:
            c = 4
        # 绘制线条
        for i in range(random.randrange(c - 2, c)):
            line_color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
            xy = (
                random.randrange(0, self.img_width * 0.2),
                random.randrange(10, self.img_height * 0.8),
                random.randrange(self.img_width * 0.8, self.img_width),
                random.randrange(0, self.img_height)
            )
            draw.line(xy, fill=line_color, width=int(self.font_size * 0.12))
        # 绘制噪点
        for i in range(random.randrange(20, 35)):
            draw.point([random.randint(0, self.img_width), random.randint(0, self.img_height)],
                       fill=self._get_random_color())
            a = random.randint(0, self.img_width)
            b = random.randint(0, self.img_height)
            draw.arc((a, b, a + 5, b + 5), 0, 90, fill=self._get_random_color())
        # 绘制验证码
        j = int(self.font_size * 0.3)
        k = int(self.font_size * 0.5)
        x = random.randrange(j, k)
        for i in self.code:
            m = int(len(self.code))
            y = random.randrange(3, 30)
            if i in ('+', '=', '?'):
                m = ceil(self.font_size * 0.3)
            else:
                m = random.randrange(0, int(40 / self.font_size) + int(self.font_size / 3))
            self.font = ImageFont.truetype(self.font_path.replace('\\', '/'), self.font_size + int(ceil(m)))
            draw.text((x, y), i, font=self.font, fill=random.choice(self.font_colors))
            x += self.font_size
        del x
        del draw
        # 序列化
        buf = BytesIO()
        im.save(buf, 'gif')
        buf.closed
        return buf.getvalue()

    def validate(self, code):
        """校验用户输入的是否与服务器端一致"""
        if not code:
            return False
        _code = self.django_request.session.get(self.session_key) or ''
        self.django_request.session[self.session_key] = ''
        return _code == int(code)
