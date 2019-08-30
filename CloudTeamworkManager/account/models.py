from django.db import models
from django.contrib.auth.models import User,AbstractUser,AbstractBaseUser


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 5, verbose_name = '姓名')
    birthday = models.CharField(max_length = 10, verbose_name = '生日')
    sex = models.CharField(max_length = 1, choices=(('m','男'),('f','女')), verbose_name = '性别')
    student_id = models.CharField(max_length = 11, verbose_name = '学号',unique=True)
    cloud_id = models.CharField(max_length = 20, verbose_name = '云顶号')
    email = models.CharField(max_length = 30, verbose_name = '邮箱')
    major = models.CharField(max_length = 1, choices=(('M','机电创新团队'), ('P','Python'),('N','Node.js'), 
                                                      ('J','Java'), ('F','前端'), ('D','设计')), verbose_name = '方向')
    grade = models.CharField(max_length = 4, verbose_name = '年级')
    room = models.CharField(max_length = 8, verbose_name = '宿舍号')
    home_address = models.CharField(max_length = 100, verbose_name = '家庭住址', default = "")
    guardian_phone = models.CharField(max_length = 11, verbose_name = '家长手机号', default = "")
    introduction = models.CharField(max_length = 350, verbose_name = '个人介绍', default = "")
    involved_projects = models.TextField(default = "[]")
    involved_projects_number = models.IntegerField(default = 0)
    managed_projects = models.TextField(default = "[]")
    managed_projects_number = models.IntegerField(default = 0)
    read_notifications = models.TextField(default = "[]")
    unread_notifications = models.TextField(default = "[]")


    def __str__(self):
        return '{}·{}·{}'.format(self.major,self.name,self.student_id)

    class Meta:
        verbose_name=u'用户信息'
        verbose_name_plural = verbose_name