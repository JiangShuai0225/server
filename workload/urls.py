"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns: path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns: path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include,path
    2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path

urlpatterns = [
  path('api/login',views.login, name='login'),  # ok
  path('api/token/verify',views.token_verify,name='token_verify'),
  path('api/home', views.home, name='home'), # 
  path('api/user/list', views.userlist, name='userlist'), # ok
  path('api/user/add', views.useradd, name='useradd'), # ok
  path('api/user/edit', views.useredit, name='useredit'), # ok
  path('api/user/password/update', views.updatepassword, name='updatepassword'), # ok
  path('api/user/leave', views.userleave, name='userleave'), # ok
  path('api/user/leave/list', views.userleavelist, name='userleavelist'), # ok
  path('api/user/leave/audit', views.leaveaudit, name='leaveaudit'), # ok
  path('api/user/banned', views.banned, name='banned'), # ok
  
  path('api/ticket/list', views.ticketlist, name='ticketlist'), # ok
  path('api/ticket/detail', views.ticketdetail, name='ticketdetail'), # ok
  path('api/ticket/create', views.ticketcreate, name='ticketcreate'), # 预留接口 ok
  path('api/ticket/distribute', views.ticketdistribute, name='ticketdistribute'), # 分配工单手动 ok
  path('api/ticket/end', views.ticketend, name='ticketend'), # 结束工单 ok
  path('api/ticket/check', views.ticketcheck, name='ticketcheck'), # 工单状态检查 ok
  path('api/ticket/decument', views.ticketdecument, name='ticketdecument'), # 工单文档上传 ok
]
