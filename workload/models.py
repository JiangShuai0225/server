from django.db import models
import uuid
# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=20) # 用户名
    password = models.CharField(max_length=40) # 密码
    nickname = models.CharField(max_length=20) # 姓名
    banned = models.BooleanField(default=False) # 帐号状态
    status = models.IntegerField(default=1) # 1 空闲 2 忙碌 0 休假
    telephone = models.CharField(max_length=20) # 电话
    role = models.IntegerField(default=0) # 0普通用户 1管理员
    last_time = models.IntegerField(default=0) # 最后一次完成时间
    class Meta:
        db_table = 'users'

class Tickets(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid1)
    url = models.CharField(max_length=100,db_index=True) 
    user = models.IntegerField(default=0)
    message = models.CharField(max_length=200,default='') # 备注
    status = models.IntegerField(default=0) # 0未派发 1进行中 2已完成
    create_time = models.IntegerField(default=0)
    start_time = models.IntegerField(default=0)
    end_time = models.IntegerField(default=0)
    code = models.TextField(max_length=30000,default='') # 代码
    class Meta:
        db_table = 'tickets'

class UserTicket(models.Model):
    user = models.IntegerField(default=0) # 用户id
    total = models.IntegerField(default=0) # 累计完成工单数量
    years = models.CharField(max_length=20) # 年月
    class Meta:
        db_table = 'user_ticket'

class UserLeave(models.Model):
    user = models.IntegerField(default=0) # 用户id
    status = models.IntegerField(default=0) # 0未审核 1已批准 2 已拒绝 
    reason = models.CharField(max_length=200) # 请假原因
    create_time = models.IntegerField(default=0) # 申请时间
    start_time = models.IntegerField(default=0) # 开始时间
    end_time = models.IntegerField(default=0) # 结束时间
    class Meta:
        db_table = 'user_leave'
        
