from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views import View

from meiduo.utils.views import LoginVerifyMixin
from users.models import User, Address
from django_redis import get_redis_connection
import json
import re,logging
logger = logging.getLogger('django')
from django.contrib.auth import login, authenticate, logout
from celery_tasks.email.tasks import send_verify_email


#用户名重复注册验证
class UsernameCountView(View):
    def get(self,request,username):
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            return JsonResponse({'code':400, 'errmsg':'访问服务器失败'})
        return JsonResponse({'code':200,'errmsg':'ok','count':count})

#手机号重复注册验证
class MobileCountView(View):
    def get(self,request,mobile):
        try:
            count = User.objects.filter(mobile=mobile).count()
        except Exception as e:
            return JsonResponse({'code':400,'errmsg':'查询出错'})
        return JsonResponse({'code':200,'errmsg':'ok','count':count})

#注册接口
class RegisterView(View):
    def post(self,request):
        # 1.接受数据
        dict = json.loads(request.body.decode())
        # 2.提取参数
        username = dict.get('username')
        password = dict.get('password')
        password2 = dict.get('password2')
        mobile = dict.get('mobile')
        allow = dict.get('allow')
        sms_code_client = dict.get('sms_code')
        # 3.检验参数(整体)
        if not all([username,password,password2,mobile,allow,sms_code_client]):
            return JsonResponse({'code':400,'errmsg':'传入参数缺少'})
        # 4.检验参数(单个)
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$',username):
            return JsonResponse({'code': 400, 'errmsg': 'username格式有误'})
        if not re.match(r'^[a-zA-Z0-9]{8,20}$',password):
            return JsonResponse({'code': 400,  'errmsg': 'password格式有误'})
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次输入不对'})
        if not re.match(r'^1[3-9]\d{9}$',mobile):
            return JsonResponse({'code': 400,'errmsg': 'mobile格式有误'})
        if allow==False:
            return JsonResponse({'code': 400, 'errmsg': 'allow格式有误'})

        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s'%mobile)
        if sms_code_server is None:
            return JsonResponse({'code': 400,'errmsg': '短信验证码过期'})
        if sms_code_client != sms_code_server.decode():
            return JsonResponse({'code': 400, 'errmsg': '验证码有误'})
        # 5.保存用户
        try:
            user = User.objects.create_user(username=username,password=password,mobile=mobile)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '保存到数据库出错'})
        # 6.状态保持
        login(request,user)
        # 登录后显示用户名
        # 通过cookie携带用户信息
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username',user.username,max_age=3600*24*12)
        # 7.返回响应
        return response

#登录接口
class LoginView(View):
    def post(self,request):
        #1.接受请求,提取参数
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        remembered = dict.get('remembered')
        #2.检验参数(整体检验)
        if not all([username,password]):
            return JsonResponse({'code':400,'errmsg':'缺少必传参数'})
        #3.登录认证authenticate
        user = authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({'code': 400,'errmsg': '用户名或者密码错误'})
        #4.保持状态login
        login(request,user)
        #5.判断是否需要记住登录
        if remembered == True:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)

        response = JsonResponse({'code':0,'errmsg':'ok'})
        response.set_cookie('username',user.username,max_age=3600*24*12)

        #6.返回响应
        return response


#退出登录接口
class LogoutView(View):
    def delete(self,request):
        '''实现退出登录逻辑'''
        #清理session
        logout(request)

        #创建response对象, 删除cookie信息
        response = JsonResponse({'code':0,'errmsg':'ok'})
        response.delete_cookie('username')
        return response


#用户信息中心接口
class UserInfoView(LoginVerifyMixin,View):
    def get(self,request):
        dict = {'username':request.user.username,
                'mobile':request.user.mobile,
                'email':request.user.email,
                'email_active':request.user.email_active,
                }
        return JsonResponse({'code':0,'errmsg':'ok','info_data':dict})


#实现添加邮箱逻辑
class EmailView(View):
    def put(self,request):
        #1.接受请求,提取参数
        dict = json.loads(request.body.decode())
        email = dict.get('email')
        #2.验证参数(整体)
        if email is None:
            return JsonResponse({'code': 400,  'errmsg': '缺少email参数'})
        #3.验证参数(单个)
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return JsonResponse({'code': 400, 'errmsg': '参数email有误'})
        #4.赋值email字段
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400,  'errmsg': '添加邮箱失败'})
        #5.todo 发送验证邮件功能
        try:
            verify_url = request.user.generate_verify_email_url()
            send_verify_email.delay(email,verify_url)
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 0,  'errmsg': '发送邮箱失败'})

        return JsonResponse({'code': 0,  'errmsg': 'ok'})


#验证邮箱链接
class VerifyEmailView(View):
    def put(self,request):
        #接受请求,提取参数
        token = request.GET.get('token')
        #验证参数(整体)
        if not token:
            return JsonResponse({'code':400, 'errmsg':'缺少token'})
        #通过token返回用户模型类对象
        user = User.check_verify_email_url(token)
        #判断user是否存在
        if not user:
            return JsonResponse({'code':400, 'errmsg':'无效的token'})
        #修改email_active激活字段值
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code':400, 'errmsg':'激活邮件失败'})
        return JsonResponse({'code':0,  'errmsg':'ok'})


#新增地址接口
class CreateAddressView(View):
    def post(self,request):
        #先查看地址个数
        try:
            count = Address.objects.filter(user=request.user,is_deleted=False).count()
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '获取地址数据出错'})
        if count >= 20:  # 判断是否超过地址上限：最多20个
            return JsonResponse({'code': 400, 'errmsg': '超过地址数量上限'})
        #提取参数
        dict = json.loads(request.body.decode())
        receiver = dict.get('receiver')
        province_id = dict.get('province_id')
        city_id = dict.get('city_id')
        district_id = dict.get('district_id')
        place = dict.get('place')
        mobile = dict.get('mobile')
        tel = dict.get('tel')
        email = dict.get('email')
        #验证参数(整体)
        if not all([receiver,province_id,city_id,district_id,place,mobile]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})
        #验证参数(单个)
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '参数mobile有误'})
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return JsonResponse({'code': 400, 'errmsg': '参数tel有误'})
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return JsonResponse({'code': 400, 'errmsg': '参数email有误'})
        #保存地址信息
        try:
            address = Address.objects.create(user=request.user, title=receiver, receiver=receiver,
                                             province_id=province_id, city_id=city_id, district_id=district_id,
                                             place=place, mobile=mobile, tel=tel, email=email)
        #设置默认地址
            if not request.user.default_address:
                request.user.default_address = address
                request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400, 'errmsg': '新增地址失败'})
        #返回响应
        return JsonResponse({'code': 0,  'errmsg': '新增地址成功',  'address':0})


#展示地址接口
class AddressView(View):
    def get(self,request):
        #从数据库获取数据
        try:
            address_set = Address.objects.filter(user=request.user, is_deleted=False)
            #把查询集遍历存入列表
            address_list = []
            for address_sub in address_set:
                address_dict = {"id": address_sub.id, "title": address_sub.title,"receiver": address_sub.receiver,"province": address_sub.province.name, "city": address_sub.city.name, "district": address_sub.district.name,"place": address_sub.place,"mobile": address_sub.mobile, "tel": address_sub.tel, "email": address_sub.email}
                #若该地址是默认地址, 插在最前
                if request.user.default_address_id == address_sub.id:
                    address_list.insert(0,address_dict)
                #若不是, 追加后面
                else:
                    address_list.append(address_dict)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '展示地址失败'})
        #提取用户默认id
        default_id = request.user.default_address_id
        return JsonResponse({'code':0,'errmsg':'ok', 'addresses':address_list,'default_address_id':default_id})