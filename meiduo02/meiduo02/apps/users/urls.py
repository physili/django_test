
from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    re_path(r'^register/$', views.RegisterView.as_view()),
    re_path(r'^login/$', views.LoginView.as_view()),
    re_path(r'^logout/$', views.LogoutView.as_view()),
    re_path(r'^info/$', views.UserInfoView.as_view()),
    re_path(r'^emails/$', views.EmailView.as_view()),
    re_path(r'^emails/verification/$', views.VerifyEmailView.as_view()),
    re_path(r'^addresses/create/$', views.CreateAddressView.as_view()),
    re_path(r'^addresses/$', views.AddressView.as_view()),
    re_path(r'^addresses/(?P<address_id>\d+)/$', views.UpdateDestroyAddressView.as_view()),
    re_path(r'^addresses/(?P<address_id>\d+)/default/$', views.DefaultAddressView.as_view()),
    re_path(r'^addresses/(?P<address_id>\d+)/title/$', views.UpdateTitleAddressView.as_view()),
    re_path(r'^password/$', views.ChangePasswordView.as_view()),
]
