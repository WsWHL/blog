from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def send_email_confirm(host, to_email, token):
    """
    发送邮箱确认信息
    :return:
    """

    subject = '来自This Blog的注册确认邮件'
    text_content = '''欢迎注册This Blog，一位专注于技术分享的佛系程序猿！\
                        如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''.format(host)
    html_content = '''
                        <p>感谢注册<a href="{}/confirm/{}" target=blank>This Blog</a>，\
                        这里是This Blog的个人博客，专注于技术分享。</p>
                        <p>请点击站点链接完成注册确认！</p>
                        <p>此链接有效期为{}天！</p>
                        '''.format(host, token, settings.EMAIL_CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
