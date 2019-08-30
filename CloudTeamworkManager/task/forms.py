import re
from django.forms import ModelForm, ValidationError
from django.contrib.auth.models import User
from django import forms
from .models import task as models_task

class task(ModelForm):
    class Meta:
        model = models_task
        exclude = ("appendixes", "task_comment", "creator", "publish_date", "task_schedule", "task_progress", "all_members")

    def __init__(self, *args, **kwargs):
        super(task, self).__init__(*args, **kwargs)
        self.fields["task_description"].required = False
        self.fields["task_need"].required = False
        self.fields["leaders"].required = False

    #def clean_deadline(self):
    #    deadline = self.cleaned_data["deadline"]

    #    if re.match('\d{4}-\d{2}-\d{2}', deadline):
    #        return deadline
    #    raise validationerror("截止日期不正确")

    #def clean_task_status(self):
    #    task_status = self.cleaned_data['task_status']

    #    if task_status in [0, -1, 1]:
    #        return task_status
    #    raise validationerror("任务状态不正确") 
