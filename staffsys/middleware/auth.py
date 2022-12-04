from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthLoginMiddleware(MiddlewareMixin):

    def process_request(self, request):

        # 0.排除不需要session也可以显示的页面，不然login会进入死循环
        # request.path_info('')

        if request.path_info in ["/login/", "/image/code/"]:
            return

        # 1. 读取当前访问的用户session信息，如果有，表示已经登陆过，可以进行放行
        # 该info是来自于登陆的视图文件：account中
        login_info_dict = request.session.get("info")
        if login_info_dict:
            return

        return redirect('/login/')
