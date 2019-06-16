# 获取IP地址
def get_client_ip(request):
    x_forwarded_for = request.META.get('X_FORWARDED_FOR')
    if x_forwarded_for is None:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
