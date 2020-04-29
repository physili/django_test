from django.contrib.auth import login,authenticate,logout

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django_redis import get_redis_connection
from meiduo02.utils.views import LoginVerifyMixin
from celery_tasks.email.tasks import send_verify_email
import logging
logger = logging.getLogger('django')
from users.models import User2, Address
import re
import json

# Create your views here.
#用户名重复验证接口
class UsernameCountView(View):
    '''判断用户是否重复'''
    def get(self,request,username):
        '''判断用户名是否重复'''
    # 1.查询username在数据库中的个数
        try:
            count = User2.objects.filter(username=username).count()
        except Exception as e:
            return JsonResponse({'code':400,'errmsg':'访问数据库失败'})
    # 2.返回结果json-->code&errmsg&count
        return JsonResponse({'code':200,'errmsg':'ok','count':'count'})

#手机号重复验证接口
class MobileCountView(View):
    '''判断手机号是否重复'''
    def get(self,request,mobile):
        '''判断手机号是否重复'''
        try:
            count = User2.objects.filter(mobile=mobile).count()
        except Exception as e:
            return JsonResponse({'code':400,'errmsg':'访问数据库失败'})
        return JsonResponse({'code':200,'errmsg':'ok','count':'count'})

#注册接口
class RegisterView(View):
    def post(self,request):
        #1.接受请求, 提取参数(username,password,psd2,mobile,sms_code,allow)
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        password2 = dict.get('password2')
        mobile = dict.get('mobile')
        allow = dict.get('allow')
        sms_code_client = dict.get('sms_code')
        #2.验证参数(整体验证)
        if not all([username,password,password2,mobile,allow,sms_code_client]):
            return JsonResponse({'code':400,'errmsg':'缺少必传参数'})
        #3.单个验证参数
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$',username):
            return JsonResponse({'code': 400, 'errmsg': 'username格式有误'})
        if not re.match(r'^[a-zA-Z0-9]{8,20}$',password):
            return JsonResponse({'code': 400,  'errmsg': 'password格式有误'})
        if password2 != password:
            return JsonResponse({'code': 400, 'errmsg': '两次输入不对'})
        if not re.match(r'^1[3-9]\d{9}$',mobile):
            return JsonResponse({'code': 400,'errmsg': 'mobile格式有误'})
        if allow == False:
            return JsonResponse({'code': 400, 'errmsg': 'allow格式有误'})
        #3.1验证短信码
        #3.1.1提取短信验证码
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s'%mobile)
        #3.1.2判断是否过期无效
        if sms_code_server is None:
            return JsonResponse({'code': 400,'errmsg': '短信验证码过期'})
        #3.1.3判断sms_code是否正确
        if sms_code_client != sms_code_server.decode():
            return JsonResponse({'code': 400, 'errmsg': '验证码有误'})
        #4.保存数据到MySQL(try),用模型类
        try:
            user = User2.objects.create_user(username=username,password=password,mobile=mobile)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '保存到数据库出错'})
        #5.状态保存, 生成session返回,用login
        login(request,user)
        #用cookie携带用户user的信息返回, 展示用户名信息
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username',user.username,max_age=3600*24*12)
        #6.返回响应
        return response

#登录接口
class LoginView(View):
    def post(self,request):
        #1.接受请求,提取参数(username,password,remembered)
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        remembered = dict.get('remembered')
        #2.验证参数(整体)
        if not all([username,password,remembered]):
            return JsonResponse({'code':400,'errmsg':'缺少必传参数'})
        #3.验证username和password用authenticate
        #3.2判断user是否存在
        user = authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({'code':400,'errmsg':'验证失败'})
        #4.保持状态
        login(request,user)
        #5.判断是否remembered
        if remembered == True:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)
        #6.cookie携带用户名信息,显示信息
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', user.username, max_age=3600*24*12)
        #7.响应返回
        return response


#登录退出接口
class LogoutView(View):
    def delete(self,request):
        logout(request)

        response = JsonResponse({'code':0,'errmsg':'ok'})
        response.delete_cookie('username')
        return response


#用户信息中心
class UserInfoView(LoginVerifyMixin,View):
    def get(self,request):
        #提取用户中心信息
        info_dict = {
            'username':request.user.username,
            'mobile':request.user.mobile,
            'email':request.user.email,
            'email_active':request.user.email_active,
        }
        return JsonResponse({'code':0,'errmsg':'ok','info_data':info_dict})


#添加邮箱接口
class EmailView(View):
    def put(self,request):
        #接受请求,提取参数
        dict = json.loads(request.body.decode())
        email = dict.get('email')
        #验证参数(整体)
        if not email:
            return JsonResponse({'code': 400,  'errmsg': '缺少email参数'})
        #验证参数(单个)
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return JsonResponse({'code': 400, 'errmsg': '参数email有误'})
        #email赋值
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400,  'errmsg': '添加邮箱失败'})
        #todo email发送
        #先在上面导入异步任务函数
        verify_url = request.user.generate_verify_email_url()
        send_verify_email.delay(email,verify_url)
        #响应返回
        return JsonResponse({'code': 0,  'errmsg': 'ok'})

#验证邮箱链接接口
class VerifyEmailView(View):
    def put(self,request):
        #接受请求,提取参数
        token = request.GET.get('token')
        #验证参数
        if not token:
            return JsonResponse({'code':400, 'errmsg':'缺少token'})
        user = User2.check_verify_email_token(token)
        #判断user是否存在
        if not user:
            return JsonResponse({'code':400, 'errmsg':'无效的token'})
        #提取user的email_active, 并改成True
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
        #获取地址个数, 先判断是否超20个
        try:
            address_count = Address.objects.filter(user=request.user, is_deleted=False).count()
        except Exception as e:
            return JsonResponse({'code': 400,  'errmsg': '获取地址数据出错'})
        if address_count >= 20:
            return JsonResponse({'code': 400,  'errmsg': '超过地址数量上限'})
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
        #验证参数(整体:receiver,province_id,city_id,district_id,place,mobile
        if not all([receiver,province_id,city_id,district_id,place,mobile]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})
        #验证参数(单个:mobile,tel,email)
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
            address = Address.objects.create(user=request.user, title = receiver, receiver = receiver,province_id = province_id,city_id = city_id, district_id = district_id, place = place,mobile = mobile,tel = tel,email = email)
            # 设置默认地址, 先判断user是否有默认地址
            if not request.user.default_address:
                request.user.default_address = address
                request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400, 'errmsg': '新增地址失败'})
        #返回新增数据
        address_dict = {"id": address.id, "title": address.title, "receiver": address.receiver,
                        "province": address.province.name, "city": address.city.name, "district": address.district.name,
                        "place": address.place, "mobile": address.mobile, "tel": address.tel, "email": address.email}
        return JsonResponse({'code': 0, 'errmsg': '新增地址成功', 'address': address_dict})


#展示用户收货地址接口
class AddressView(View):
    def get(self,request):
        #从数据库提取地址数据对象
        addresses = Address.objects.filter(user=request.user,is_deleted=False)
        #把对象转化成列表格式返回
        address_list = []
        for address in addresses:
            address_dict = {"id": address.id, "title": address.title,"receiver": address.receiver,
                            "province": address.province.name, "city": address.city.name, "district": address.district.name,
                            "place": address.place,"mobile": address.mobile, "tel": address.tel, "email": address.email}
            #将默认地址移动到最前面
            if request.user.default_address_id == address.id:
                address_list.insert(0,address_dict)
            else:
                address_list.append(address_dict)
        #提取默认地址id返回
        default_id = request.user.default_address_id
        #返回数据
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'addresses': address_list, 'default_address_id': default_id})



