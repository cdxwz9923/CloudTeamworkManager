from django.db import models
from task.models import task as Task

class personal_comment(models.Model):
    detail = models.TextField(verbose_name = '个人评论内容', default = "[]")
    id = models.CharField(max_length = 15, primary_key = True)
    class Meta:
        verbose_name = u'个人参与任务详情'
        verbose_name_plural = verbose_name

    # 个人参与任务详情应包括：正在参与任务、历史完成任务
    # task = Task.objects.filter(id=self.id)

class personal_progress(models.Model):
    detail = models.TextField(verbose_name = '个人进度内容')
    id = models.CharField(max_length = 15, primary_key = True, default = "[]")

    class Meta:
        permissions = {
            #('view_personal_progress', '查看个人进度'), 
            ('edit_personal_progress', '编辑个人进度'), 
        }
        verbose_name = u'个人进度'
        verbose_name_plural = verbose_name

class personal_schedule(models.Model):
    detail = models.TextField(verbose_name = '个人时间表内容', default = "[]")
    id = models.CharField(max_length = 15, primary_key = True)

    class Meta:
        permissions = {
            #('view_personal_schedule', '查看个人时间表'), 
            ('edit_personal_schedule', '编辑个人时间表'), 
        }
        verbose_name = u'个人时间表'
        verbose_name_plural = verbose_name