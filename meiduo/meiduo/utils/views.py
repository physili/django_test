from django import http

#装饰器,判断用户是否登录
def my_decorator(view):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return view(request,*args,**kwargs)
        else:
            return http.JsonResponse({'code':400, 'errmsg':'请登录后重试'})
    return inner

#Mixin扩展类
class LoginVerifyMixin(object):
    @classmethod
    def as_view(cls,*args, **kwargs):
        view = super().as_view(*args, **kwargs)
        return my_decorator(view)