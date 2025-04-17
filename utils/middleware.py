from django.urls import include
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 运行直接访问地址
        if request.path_info in ["/login/"] or request.path_info.startswith("/captcha/"):
            return

        # 若存在登入信息，可访问
        info_dict = request.session.get("info")
        if info_dict:
            request.info_dict = info_dict
            return

        # 未登入
        return redirect("/login/")
