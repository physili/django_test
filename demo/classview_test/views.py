# 导入模块是固定格式
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# Create your views here.


def my_decorator_3(func):
    def wrapper(request, *args, **kwargs):
        print('自定义装饰器被调用了3')
        print('请求路径%s' % request.path)
        return func(request, *args, **kwargs)
    return wrapper
# 我们自定义的装饰器:
def my_decorator_33(func):
    def wrapper(request, *args, **kwargs):
        print('自定义装饰器被调用了33')
        print('请求路径%s' % request.path)
        return func(request, *args, **kwargs)
    return wrapper

class FirstMixin3(object):
    """ FirstMixin 扩展类 """
    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        view = my_decorator_3(view)
        return view
class SecondMixin3(object):
    """ SecondMixin 扩展类 """
    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        view = my_decorator_33(view)
        return view

# class View(object):
    # @classonlymethod
    # def as_view(cls, **initkwargs):
    #     def view(request, *args, **kwargs):
    #         return self.dispatch(request, *args, **kwargs)
    #     return view
    # def dispatch(self, request, *args, **kwargs):
    #     return handler(request, *args, **kwargs)

# views.TestView.as_view()
# TestView继承了FirstMixin, View ==> 故可以调用父类的as_view()方法
# 然后根据mro顺序调用,
# 去到View类时得到==> views.TestView.view
# 回到Second得到 ==> views.TestView.my_decorator_33(view)
# 再回到First得到==>views.TestView.my_decorator_3(my_decorator_33(view))
# 然后先执行装饰器my_decorator_3
# 再执行装饰器my_decorator_33

class TestView(FirstMixin3, SecondMixin3, View):
    '''类视图'''
    # get方法,固定格式
    def get(self,request):
        print('get')
        return HttpResponse('get_TestView')

    # post方法,也是固定格式
    def post(self,request):
        print('post')
        return HttpResponse('post_TestView')


# 第二版
def my_decorator_2(func):
    def wrapper(request, *args, **kwargs):
        print('自定义装饰器被调用了111')
        print('请求路径%s' % request.path)
        return func(request, *args, **kwargs)
    return wrapper

class FirstMixin2(object):
    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        view = my_decorator_1(view)
        return view

# class View(object):
    # @classonlymethod
    # def as_view(cls, **initkwargs):
    #     def view(request, *args, **kwargs):
    #         return self.dispatch(request, *args, **kwargs)
    #     return view
    # def dispatch(self, request, *args, **kwargs):
    #     return handler(request, *args, **kwargs)

# views.TestView.as_view()
# TestView继承了FirstMixin, View ==> 故可以调用父类的as_view()方法
# 然后根据mro顺序调用, 去到View类时得到==> views.TestView.view

class TestView2(FirstMixin2, View):
    '''类视图'''
    # get方法,固定格式
    def get(self,request):
        print('get')
        return HttpResponse('get_TestView')

    # post方法,也是固定格式
    def post(self,request):
        print('post')
        return HttpResponse('post_TestView')




# 第一版
class TestView1(View):
    '''类视图'''
    # get方法,固定格式
    def get(self,request):
        print('get')
        return HttpResponse('get_TestView')

    # post方法,也是固定格式
    def post(self,request):
        print('post')
        return HttpResponse('post_TestView')