from django import template
import re

register = template.Library()

email = re.compile(r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}')
phone = re.compile(r'0?(13|14|15|18|17)[0-9]{9}')


@register.filter
def usersafe(value):
    """
    用户账户安全过滤器
    """
    if value and len(value) > 0:
        result = email.match(value)
        if result:
            contents = result[0].split('@')
            if contents and len(contents) >= 2:
                return '%s***@%s' % (contents[0][0:int(len(contents[0]) / 2)], contents[1])
            return result[0]
        result = phone.match(value)
        if result:
            return result[0]
    return value