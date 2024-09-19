import time
import zlib
from django.shortcuts import render
import orjson
import uuid  
import datetime
from django.http import JsonResponse
import jwt
from .models import *
from server import settings
from django.db.models import Q



def token_verify(request):
  payload = request.payload
  return JsonResponse({ 'status': True, 'message': '', 'data': payload })

# Create your views here.

def login(request):
  username = request.data.get('username')
  password = request.data.get('password')
  try:
    user = Users.objects.get(username=username,password=password)
    if user.banned == 1:
      return JsonResponse({'status': False, 'message': '账号已被封禁', 'data': {}})
    
    payload = {
      'id': user.id,
      'username': user.username,
      'role': user.role,
      'status': user.status,
      'exp': datetime.datetime.now() + datetime.timedelta(weeks=52)
    }
    
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return JsonResponse({'status': True, 'message': '登录成功', 'data': {'token': token}})
  except Users.DoesNotExist:
    return JsonResponse({ 'status': False, 'message': '账号或密码错误', 'data': {} })

def home(request): # 总共单数，待分配工单数， 待处理工单数 ， 已完成工单数，今日在线人数， 今日新增工单数， 今日已处理工单数， 今日请假人数
  today = int(datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d').timestamp()) - 1577808000
  ticket_total= Tickets.objects.count()
  ticket_unhandled = Tickets.objects.filter(status=0).count()
  ticket_handled = Tickets.objects.filter(status=1).count()
  ticket_finished = Tickets.objects.filter(status=2).count()
  ticket_today_created = Tickets.objects.filter(create_time__gte=today).count()
  ticket_today_end = Tickets.objects.filter(end_time__gte=today).count()
  user_online = Users.objects.filter(status=1 | 2).count()
  user_leave = Users.objects.filter(status=0).count()
  data = {
    'ticket_total': ticket_total,
    'ticket_unhandled': ticket_unhandled,
    'ticket_handled': ticket_handled,
    'ticket_finished': ticket_finished,
    'ticket_today_created': ticket_today_created,
    'ticket_today_end': ticket_today_end,
    'user_online': user_online,
    'user_leave': user_leave,
  }
  return JsonResponse({'status': True, 'message': '', 'data': { 'data': data }})

def userlist(request):
  role = request.payload.get('role')
  if role == 1:
    users = Users.objects.filter(Q(status=0) | Q(status=1) | Q(status=2)).iterator()
    data = [
      {
        'id': user.id,
        'username': user.username,
        'nickname': user.nickname,
        'status': user.status,
        'role': user.role,
        'banned': user.banned,
        'telephone': user.telephone,
      } for user in users
    ]
  else:
    data = []
  return JsonResponse({'status': True, 'message': '', 'data': { 'data': data }})


def useradd(request):
  role = request.payload.get('role')
  if role != 1:
    return JsonResponse({'status': False, 'message': '权限不足', 'data': {}})
  username = request.data.get('username')
  nickname = request.data.get('nickname')
  password = request.data.get('password')
  telephone = request.data.get('telephone')
  role = request.data.get('role')
  try:
    user = Users.objects.get(username=username)
    return JsonResponse({'status': False, 'message': '用户名已存在', 'data': {}})
  except Users.DoesNotExist:
    user = Users(username=username, nickname=nickname, password=password, telephone=telephone, role=role)
    user.save()
    return JsonResponse({'status': True, 'message': '添加成功', 'data': {}})

def useredit(request):
  role = request.payload.get('role')
  ID = request.payload.get('id')
  id = request.data.get('id')
 
  if role != 1 & ID != id:
    return JsonResponse({'status': False, 'message': '权限不足', 'data': {}})
  try:
    user = Users.objects.get(id=id)
    print(user)
    nickname = request.data.get('nickname') 
    telephone = request.data.get('telephone')
    print(nickname, telephone)
    if role == 1:
      user_role = request.data.get('role')
      status = request.data.get('status')
      user.role = user_role
      user.status = status
      print(user_role, status)
    user.nickname = nickname
    user.telephone = telephone
    user.save()
    print('okok')
    return JsonResponse({'status': True, 'message': '修改成功', 'data': {}})
  except Users.DoesNotExist:
    return JsonResponse({'status': False, 'message': '用户不存在', 'data': {}})

def updatepassword(request):
  role = request.payload.get('role')
  ID = request.payload.get('id')
  id = request.data.get('id')
  password = request.data.get('password')
  if role != 1 & ID != id:
    return JsonResponse({'status': False, 'message': '权限不足', 'data': {}})
  try:
    user = Users.objects.get(id=id)
    user.password = password
    user.save()
    return JsonResponse({'status': True, 'message': '修改成功', 'data': {}})
  except Users.DoesNotExist:
    return JsonResponse({'status': False, 'message': '用户不存在', 'data': {}})

def userdel(request):
  role = request.payload.get('role')
  id = request.data.get('id')
  if role != 1:
    return JsonResponse({'status': False, 'message': '权限不足', 'data': {}})
  try:
     user = Users.objects.get(id=id)
     user.delete()
     return JsonResponse({'status': True, 'message': '删除成功', 'data': {}})
  except Users.DoesNotExist:
    return JsonResponse({'status': False, 'message': '用户不存在', 'data': {}})
  
def userleave(request):
  id = request.data.get('id')
  reason = request.data.get('reason')
  start_time = int(datetime.datetime.strptime(request.data.get('start_time'), "%Y-%m-%d %H:%M:%S").timestamp()) - 1577808000
  end_time = int(datetime.datetime.strptime(request.data.get('end_time'), "%Y-%m-%d %H:%M:%S").timestamp()) - 1577808000
  create_time = int(datetime.datetime.now().timestamp()) - 1577808000
  try:
    UserLeave.objects.create(user=id, reason=reason, start_time=start_time, create_time=create_time, end_time=end_time)
    return JsonResponse({'status': True, 'message': '申请成功', 'data': {}})
  except:
    return JsonResponse({'status': False, 'message': '申请失败', 'data': {}})

def userleavelist(request):
  role = request.payload.get('role')
  if role != 1:
    return JsonResponse({'status': False, 'message': '权限不足', 'data': {}})
  try:
    userleave = UserLeave.objects.all().iterator()
    data = [
      {
        'id': item.id,
        'user': item.user,
        'reason': item.reason,
        'start_time': datetime.datetime.fromtimestamp(item.start_time + 1577808000).strftime("%Y-%m-%d %H:%M:%S"),
        'end_time': datetime.datetime.fromtimestamp(item.end_time + 1577808000).strftime("%Y-%m-%d %H:%M:%S"),
        'create_time': datetime.datetime.fromtimestamp(item.create_time + 1577808000).strftime("%Y-%m-%d %H:%M:%S"),
        'status': item.status
      } for item in userleave
    ] 
    return JsonResponse({'status': True, 'message': '查询成功', 'data': { 'data': data }})
  except:
    return JsonResponse({'status': True, 'message': '暂无数据', 'data': {}})

def leaveaudit(request):
  role = request.payload.get('role')
  if role != 1:
    return JsonResponse({'status': False, 'message': '权限不足', 'data': {}})
  id = request.data.get('id')
  status = request.data.get('status')
  try:
    UserLeave.objects.filter(id=id).update(status=status)
    return JsonResponse({'status': True, 'message': '审核成功', 'data': {}})
  except:
    return JsonResponse({'status': True, 'message': '', 'data': {}})
  
# do something for test git
#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
def banned(request):
  role = request.payload.get('role')
  if role != 1:
    return JsonResponse({'status': False, 'message': '权限不足', 'data': {}})
  id = request.data.get('id')
  try:
    user = Users.objects.get(id=id)
    if user.banned == True:
      user.banned = False
    else:
      user.banned = True
    user.save()
    return JsonResponse({'status': True, 'message': '操作成功', 'data': {}})
  except:
    return JsonResponse({'status': False, 'message': '用户不存在', 'data': {}})

def ticketlist(request):
  role = request.payload.get('role')
  if role == 2:
    tickets = Tickets.objects.filter(user=request.payload.get('id')).iterator()
    data = [
      {
        'id': item.id,
        'url': item.url,
        'status': item.status,
        'message': item.message,
        'start_time': datetime.datetime.fromtimestamp(item.start_time + 1577808000).strftime('%Y-%m-%d %H:%M:%S') if item.start_time else '',
        'end_time': datetime.datetime.fromtimestamp(item.end_time + 1577808000).strftime('%Y-%m-%d %H:%M:%S') if item.end_time else '',
      } for item in tickets
    ]
    return JsonResponse({'status': True, 'message': '', 'data': { 'data': data }})
  elif role == 1:
    try:
      tickets = Tickets.objects.all().iterator()
      data = [
        {
          'id': item.id,
          'url': item.url,
          'create_time': datetime.datetime.fromtimestamp(item.create_time + 1577808000).strftime('%Y-%m-%d %H:%M:%S'),
          'status': item.status,
          'message': item.message,
          'user': item.user,
          'start_time': datetime.datetime.fromtimestamp(item.start_time + 1577808000).strftime('%Y-%m-%d %H:%M:%S') if item.start_time else '',
          'end_time': datetime.datetime.fromtimestamp(item.end_time + 1577808000).strftime('%Y-%m-%d %H:%M:%S') if item.end_time else '',
        } for item in tickets
      ] 
      return JsonResponse({'status': True, 'message': '操作成功', 'data': { 'data': data }})
    except Tickets.DoesNotExist:
      return JsonResponse({'status': True, 'message': '暂无数据', 'data': {}})

def ticketcreate(request):
  url = request.data.get('url')
  create_time = int(datetime.datetime.now().timestamp()) - 1577808000
  try:
    ticket = Tickets.objects.get(url=url)
  except Tickets.DoesNotExist:
    ticket = Tickets(url=url, create_time=create_time)

  try:
    user = Users.objects.filter(status=1, role=2).order_by('last_time').order_by('id').first()
    if user:
      ticket.user = user.id
      ticket.status = 1
      ticket.start_time = create_time
      user.status = 2
      user.save()
  except Users.DoesNotExist:
    pass
  finally:
    ticket.save()
  return JsonResponse({'status': True, 'message': '操作成功', 'data': { 'uuid': ticket.id }})
  
def ticketdistribute(request):
  role = request.payload.get('role')
  if role != 1:
    return JsonResponse({'status': False, 'message': '权限不足', 'data': {}})
  user = request.data.get('user')
  uuid = request.data.get('uuid')
  try:
    Tickets.objects.filter(id=uuid).update(user=user)
    return JsonResponse({'status': True, 'message': '分配成功', 'data': {}})
  except:
    return JsonResponse({'status': False, 'message': '操作失败', 'data': {}})

def ticketend(request): 
  uuid = request.data.get('uuid')
  id = request.payload.get('id')
  code = ','.join([ f'{i}' for i in zlib.compress(request.data.get('code').encode('utf-8')) ])
  now = datetime.datetime.now()
  years = int(datetime.datetime(now.year, now.month, 1).timestamp()) - 1577808000
  end_time = int(datetime.datetime.now().timestamp()) - 1577808000
  try:
    Tickets.objects.filter(id=uuid).update(status=2,code=code, end_time=end_time)
    user_ticket = UserTicket.objects.filter(user=id, years=years)
    if user_ticket.exists():
      user_ticket.total += 1
      user_ticket.save()
    else:
      UserTicket.objects.create(user=id, years=years, total=1)
    ticket = Tickets.objects.filter(status=0).first()
    Users.objects.filter(id=id).update(last_time = end_time)
    if ticket:
      start_time = int(datetime.datetime.now().timestamp()) - 1577808000
      ticket.user=id 
      ticket.start_time=start_time
      ticket.status=1
      ticket.save()
    else:
      Users.objects.filter(id=id).update(status=1)
    return JsonResponse({'status': True, 'message': '操作成功', 'data': {}})
  except:
    return JsonResponse({'status': False, 'message': '操作失败', 'data': {}})

def ticketcheck(request):
  uuid = request.data.get('uuid')
  try:
    status = Tickets.objects.get(id=uuid).status
    return JsonResponse({'status': status == 2, 'message': '', 'data': {}})
  except Tickets.DoesNotExist:
    return JsonResponse({'status': False, 'message': '', 'data': {}})

def ticketdecument(request):
  uuid = request.data.get('uuid')
  try:
    ticket = Tickets.objects.get(id=uuid, status=2)
    return JsonResponse({'status': True, 'message': '', 'data': {'code': ticket.code}})
  except Tickets.DoesNotExist:
    return JsonResponse({'status': False, 'message': '工单不存在', 'data': {}})

def ticketdetail(request):
  uuid = request.data.get('uuid')
  try:
    ticket = Tickets.objects.get(id=uuid)
    return JsonResponse({'status': True, 'message': '', 'data': {'code': ticket.code}})
  except Tickets.DoesNotExist:
    return JsonResponse({'status': False, 'message': '', 'data': {}})














