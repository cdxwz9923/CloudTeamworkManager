from django.db import models

class appendix(models.Model):
    name = models.CharField(max_length = 255, verbose_name = '文件名')
    upload_date = models.DateField(auto_now_add = True, verbose_name = '上传日期')
    task_id = models.IntegerField()
    publisher = models.IntegerField()
    size = models.IntegerField()

    class Meta:
        permissions = {
            ('edit_appendix', '编辑附件'),
            #('delete_appendix', '删除附件'),
        }
