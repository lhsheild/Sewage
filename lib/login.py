from django.shortcuts import redirect
from functools import wraps


def check_login(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        # 已经登录过的继续执行
        # ret = request.get_signed_cookie('is_login', default='0', salt='sewage')  # cookie
        ret = request.session.get('is_login')
        if ret == "1":
            return func(request, *args, **kwargs)
        # 没有登录的跳转到登录页
        else:
            next_url = request.path_info
            if next_url != '/logout/':
                return redirect('/login/?next={}'.format(next_url))
            else:
                return redirect('/index/')
    return inner
