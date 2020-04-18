#创建一个中间件
def my_middleware(post):
    print("中间件初始化")
    def middleware(request):
        print("所有函数准备被调用")
        result = post(request)
        print("所有已经被调用")
        return result
    return middleware