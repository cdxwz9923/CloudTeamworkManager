from django.shortcuts import render, HttpResponse, get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.contrib.auth.models import User, Group, Permission
from guardian.shortcuts import assign_perm, remove_perm
from task.models import task as models_task
from task.forms import task as forms_task
from publisher.models import personal_comment, personal_progress, personal_schedule
from account.models import UserProfile
import re
import json
import time
import os


class member(object):
    user_buildin = None
    user_profile = None
    target_task = None
    target_group = None
    target_group_leader = None

    def __init__(self, **kw):
        if "user_buildin" in kw:
            self.user_buildin = kw["user_buildin"]

        if "user_profile" in kw:
            self.user_profile = kw["user_profile"]

        if "target_task" in kw:
            self.target_task = kw["target_task"]

        if "target_group" in kw:
            self.target_group = kw["target_group"]

        if "target_group_leader" in kw:
            self.target_group_leader = kw["target_group_leader"]

    def join_task_in_profile(self):
        self.user_profile.involved_projects_number += 1
        temp = json.loads(self.user_profile.involved_projects)
        temp.append(self.target_task.id)
        temp = list(set(temp))
        self.user_profile.involved_projects = json.dumps(temp)
        self.user_profile.save()

    def quit_task_in_profile(self):
        self.user_profile.involved_projects_number -= 1
        temp = json.loads(self.user_profile.involved_projects)
        temp.remove(self.target_task.id)
        self.user_profile.involved_projects = json.dumps(temp)
        self.user_profile.save()

    def join_task_in_task(self):
        temp = json.loads(self.target_task.members)

        temp.append(self.user_buildin.id)
        temp = list(set(temp))
        self.target_task.members = json.dumps(temp)

        temp.extend(json.loads(self.target_task.all_members))
        temp = list(set(temp))
        self.target_task.all_members = json.dumps(temp)
        
        self.target_task.save()

    def quit_task_in_task(self):
        temp = json.loads(self.target_task.members)

        temp.remove(self.user_buildin.id)
        self.target_task.members = json.dumps(temp)
        
        self.target_task.save()

    def assign_member_perm(self):
        self.user_buildin.groups.add(self.target_group)

    def remove_member_perm(self):
        self.user_buildin.groups.remove(self.target_group)

    def create_personal_archive(self):
        personal_comment.objects.create(id = "%s&%s"%(self.target_task.id, self.user_buildin.id), detail = "[]")
        temp = personal_progress.objects.create(id = "%s&%s"%(self.target_task.id, self.user_buildin.id), detail = "[]")
        assign_perm('publisher.edit_personal_progress', self.user_buildin, temp)
        assign_perm('publisher.view_personal_progress', self.user_buildin, temp)
        temp = personal_schedule.objects.create(id = "%s&%s"%(self.target_task.id, self.user_buildin.id), detail = "[]")
        assign_perm('publisher.edit_personal_schedule', self.user_buildin, temp)
        assign_perm('publisher.view_personal_schedule', self.user_buildin, temp)

    def recover_archive_edit_perm(self):
        assign_perm('publisher.edit_personal_progress', self.user_buildin, personal_progress.objects.get(id = "%s&%s"%(self.target_task.id, self.user_buildin.id)))
        assign_perm('publisher.edit_personal_schedule', self.user_buildin, personal_schedule.objects.get(id = "%s&%s"%(self.target_task.id, self.user_buildin.id)))

    def remove_archive_edit_perm(self):
        remove_perm('publisher.edit_personal_progress', self.user_buildin, personal_progress.objects.get(id = "%s&%s"%(self.target_task.id, self.user_buildin.id)))
        remove_perm('publisher.edit_personal_schedule', self.user_buildin, personal_schedule.objects.get(id = "%s&%s"%(self.target_task.id, self.user_buildin.id)))

    def set_leader_in_profile(self):
        temp = json.loads(self.user_profile.managed_projects)
        temp.append(self.target_task.id)
        self.user_profile.managed_projects = json.dumps(temp)
        self.user_profile.managed_projects_number += 1
        self.user_profile.save()

    def cancel_leader_in_profile(self):
        temp = json.loads(self.user_profile.managed_projects)
        temp.remove(self.target_task.id)
        self.user_profile.managed_projects = json.dumps(temp)
        self.user_profile.managed_projects_number -= 1
        self.user_profile.save()

    def set_leader_in_task(self):
        temp = json.loads(self.target_task.leaders)
        temp.append(self.user_buildin.id)
        self.target_task.leaders = json.dumps(temp)
        self.target_task.save()

    def cancel_leader_in_task(self):
        temp = json.loads(self.target_task.leaders)
        temp.remove(self.user_buildin.id)
        self.target_task.leaders = json.dumps(temp)
        self.target_task.save()

    def assign_leader_perm(self):
        self.user_buildin.groups.add(self.target_group_leader)

    def remove_leader_perm(self):
        self.user_buildin.groups.remove(self.target_group_leader)

    def assign_creater_perm(self):
        assign_perm('task.edit_task', self.user_buildin, self.target_task)
        assign_perm('task.edit_task_comments', self.user_buildin, self.target_task)
        assign_perm('task.view_personal_comments', self.user_buildin, self.target_task)
        assign_perm('task.view_personal_progress', self.user_buildin, self.target_task)
        assign_perm('task.view_personal_schedule', self.user_buildin, self.target_task)
        assign_perm('task.edit_appendix', self.user_buildin, self.target_task)
        assign_perm('task.delete_appendix', self.user_buildin, self.target_task)

    def remove_creater_perm(self):
        remove_perm('task.edit_task', self.user_buildin, self.target_task)
        remove_perm('task.edit_task_comments', self.user_buildin, self.target_task)
        remove_perm('task.view_personal_comments', self.user_buildin, self.target_task)
        remove_perm('task.view_personal_progress', self.user_buildin, self.target_task)
        remove_perm('task.view_personal_schedule', self.user_buildin, self.target_task)
        remove_perm('task.edit_appendix', self.user_buildin, self.target_task)
        remove_perm('task.delete_appendix', self.user_buildin, self.target_task)

    def view_personal_comments(self, request):
        if request.user.has_perm("task.view_personal_comments", self.target_task):
            comment = personal_comment.objects.get(id = "%s&%s"%(self.target_task.id, self.user_buildin.id))

            return HttpResponse(comment.detail)
        return HttpResponse(status=403)
    
    def edit_personal_comments(self, request):
        if request.user.has_perm("task.edit_personal_comments", self.target_task):
            comment = personal_comment.objects.get(id = "%s&%s"%(self.target_task.id, self.user_buildin.id))
            
            if request.POST.get("action") == "upgrade":
                comment.detail = _publisher(comment.detail).upgrade(request.POST.get("content"))
            elif request.POST.get("action") == "create":
                comment.detail = _publisher(comment.detail).create(request.POST.get("content"), editor_id = request.user.id)
            comment.save()
                
            return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
        return HttpResponse(status=403)

    def view_personal_schedule(self, request):
        schedule = personal_schedule.objects.get(id = "%s&%s"%(self.target_task.id, self.user_buildin.id))

        if request.user.has_perm("publisher.view_personal_schedule", schedule) or request.user.has_perm("task.view_personal_schedule", self.target_task):
            return HttpResponse(schedule.detail)
        return HttpResponse(status=403)

    def edit_personal_schedule(self, request):
        schedule = personal_schedule.objects.get(id = "%s&%s"%(self.target_task.id, self.user_buildin.id))

        if request.user.has_perm("publisher.edit_personal_schedule", schedule):
            if request.POST.get("action") == "upgrade":
                schedule.detail = _publisher(schedule.detail).upgrade(request.POST.get("content"))
            elif request.POST.get("action") == "create":
                schedule.detail = _publisher(schedule.detail).create(request.POST.get("content"))
            schedule.save()
                
            return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
        return HttpResponse(status=403)

    def view_personal_progress(self, request):
        progress = personal_progress.objects.get(id = "%s&%s"%(self.target_task.id, self.user_buildin.id))

        if request.user.has_perm("publisher.view_personal_progress", progress) or request.user.has_perm("task.view_personal_progress", self.target_task):
            return HttpResponse(progress.detail)
        return HttpResponse(status=403)

    def edit_personal_progress(self, request):
        progress = personal_progress.objects.get(id = "%s&%s"%(self.target_task.id, self.user_buildin.id))

        if request.user.has_perm("publisher.edit_personal_progress", progress):
            if request.POST.get("action") == "upgrade":
                progress.detail = _publisher(progress.detail).upgrade(request.POST.get("content"))
            elif request.POST.get("action") == "create":
                progress.detail = _publisher(progress.detail).create(request.POST.get("content"))
            progress.save()
                
            return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
        return HttpResponse(status=403)

class task(object):
    task = None

    def __init__(self, task_id):
        self.task = models_task.objects.get(id = task_id)

    def view_task_comment(self, request):
        if request.user.has_perm("task.glance_over_task_details", self.task):
            return HttpResponse(self.task.task_comment)
        return HttpResponse(status = 403)

    def edit_task_comment(self, request):
        if request.user.has_perm("task.edit_task_comments", self.task):
            if request.POST.get("action") == "upgrade":
                self.task.task_comment = _publisher(self.task.task_comment).upgrade(request.POST.get("content"), editor_id = request.user.id)
            elif request.POST.get("action") == "create":
                self.task.task_comment = _publisher(self.task.task_comment).create(request.POST.get("content"), editor_id = request.user.id)
            self.task.save()
                
            return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
        return HttpResponse(status = 403)

    def view_task_progress(self, request):
        if request.user.has_perm("task.glance_over_task_details", self.task):
            return HttpResponse(self.task.task_progress)
        return HttpResponse(status = 403)

    def edit_task_progress(self, request):
        if request.user.has_perm("task.edit_task_progress", self.task):
            if request.POST.get("action") == "upgrade":
                self.task.task_progress = _publisher(self.task.task_progress).upgrade(request.POST.get("content"), editor_id = request.user.id)
            elif request.POST.get("action") == "create":
                self.task.task_progress = _publisher(self.task.task_progress).create(request.POST.get("content"), editor_id = request.user.id)
            self.task.save()
                
            return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
        return HttpResponse(status = 403)

    def view_task_schedule(self, request):
        if request.user.has_perm("task.glance_over_task_details", self.task):
            return HttpResponse(self.task.task_schedule)
        return HttpResponse(status = 403)

    def edit_task_schedule(self, request):
        if request.user.has_perm("task.edit_task_schedule", self.task):
            if request.POST.get("action") == "upgrade":
                self.task.task_schedule = _publisher(self.task.task_schedule).upgrade(request.POST.get("content"), editor_id = request.user.id)
            elif request.POST.get("action") == "create":
                self.task.task_schedule = _publisher(self.task.task_schedule).create(request.POST.get("content"), editor_id = request.user.id)
            self.task.save()
                
            return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
        return HttpResponse(status = 403)

    @staticmethod
    def create_page(request):
        return render(request, "create_task.html")

    @staticmethod
    def create_task(request):
        form = forms_task(request.POST)

        if form.is_valid():
            form.instance.all_members = form.instance.members
            form.instance.creator = request.user.id
            target_task = form.save()

            # 用户组
            target_group = Group.objects.create(name=str(target_task.id))
            assign_perm('task.glance_over_task_details', target_group, target_task)

            # 组长组
            target_group_leader = Group.objects.create(name = "%s%s"%(str(target_task.id), "leaders"))
            assign_perm('task.view_personal_comments', target_group_leader, target_task)
            assign_perm('task.edit_personal_comments', target_group_leader, target_task)
            assign_perm('task.edit_task_progress', target_group_leader, target_task)
            assign_perm('task.edit_task_schedule', target_group_leader, target_task)
            assign_perm('task.view_personal_progress', target_group_leader, target_task)
            assign_perm('task.view_personal_schedule', target_group_leader, target_task)
            assign_perm('task.edit_appendix', target_group_leader, target_task)
            assign_perm('task.delete_appendix', target_group_leader, target_task)

            # 配置创建者权限
            target_member = member(user_buildin = request.user, target_task = target_task, target_group = target_group, target_group_leader = target_group_leader)
            target_member.assign_member_perm()
            target_member.assign_creater_perm()

            # 配置组员相关
            for each in json.loads(form.instance.members):
                try:
                    target_member.user_buildin = User.objects.get(id = each)
                    target_member.user_profile = UserProfile.objects.get(user_id = each)
                except UserProfile.DoesNotExist:
                    continue
                except User.DoseNotExist:
                    continue

                target_member.join_task_in_profile()
                target_member.assign_member_perm()
                target_member.create_personal_archive()

            # 配置组长相关
            for each in json.loads(form.instance.leaders):
                try:
                    target_member.user_buildin = User.objects.get(id = each)
                    target_member.user_profile = UserProfile.objects.get(user_id = each)
                except UserProfile.DoesNotExist:
                    continue
                except User.DoseNotExist:
                    continue

                target_member.set_leader_in_profile()
                target_member.assign_leader_perm()

            # 建立附件目录
            os.makedirs("./file/appendixes/%s/"%(target_task.id))

            # 通知

            return JsonResponse({"task_id": target_task.id, "status": 200}, safe=False)
        return JsonResponse({"tip": "表单验证失败", "status": 400}, safe=False)

    def edit_page(self, request):
        target_task = model_to_dict(self.task, fields=["id", "task_name", "deadline", "task_status", "members", "creator", "leaders", "task_description", "task_progress", "task_schedule", "task_comment", "appendixes"])
        members = json.loads(target_task["members"])
        leaders = json.loads(target_task["leaders"])

        target_task["members"] = json.dumps([{**{"id": each}, **model_to_dict(UserProfile.objects.get(user_id = each), fields=['name', 'major'])} for each in members])
        target_task["leaders"] = json.dumps([{**{"id": each}, **model_to_dict(UserProfile.objects.get(user_id = each), fields=['name', 'major'])} for each in leaders])

        return render(request, "edit_task.html", target_task)

    def edit_task(self, request):
        form = forms_task(request.POST, instance = self.task)

        if form.is_valid():
            # 重新获取task实例，因为is_valid修改了task实例。似乎是个bug？
            self.task = models_task.objects.get(id = self.task.id)

            # 计算新增成员和被移除的成员
            past_members = set(json.loads(self.task.members))
            current_members = set(json.loads(form.instance.members))
            removed_members = past_members - current_members
            new_members = current_members - past_members

            # 计算新增组长和被移除的组长
            past_leaders = set(json.loads(self.task.leaders))
            current_leaders = set(json.loads(form.instance.leaders))
            removed_leaders = past_leaders - current_leaders
            new_leaders = current_leaders - past_leaders

            # 获取用户组
            target_group = Group.objects.get(name=str(self.task.id))
            target_group_leader = Group.objects.get(name = "%s%s"%(str(self.task.id), "leaders"))

            # 更新参与过该任务的成员列表
            form.instance.all_members = json.dumps(list(set(json.loads(form.instance.all_members) + list(current_members))))
            self.task = form.save()

            # 建立成员类
            target_member = member(target_task = self.task, target_group = target_group, target_group_leader = target_group_leader)

            # 撤销组长
            for each in removed_leaders:
                try:
                    target_member.user_buildin = User.objects.get(id = each)
                    target_member.user_profile = UserProfile.objects.get(user_id = each)
                except UserProfile.DoesNotExist:
                    continue
                except User.DoesNotExist:
                    continue

                target_member.cancel_leader_in_profile()
                target_member.remove_leader_perm()

                # 通知

            # 移除组员
            for each in removed_members:
                try:
                    target_member.user_buildin = User.objects.get(id = each)
                    target_member.user_profile = UserProfile.objects.get(user_id = each)
                except UserProfile.DoesNotExist:
                    continue
                except User.DoesNotExist:
                    continue

                target_member.quit_task_in_profile()
                target_member.remove_member_perm()
                target_member.remove_archive_edit_perm()

                # 通知

            # 配置新增组员
            for each in new_members:
                try:
                    target_member.user_buildin = User.objects.get(id = each)
                    target_member.user_profile = UserProfile.objects.get(user_id = each)
                except UserProfile.DoesNotExist:
                    continue
                except User.DoesNotExist:
                    continue

                if each in json.loads(self.task.all_members):
                    target_member.recover_archive_edit_perm()
                    target_member.join_task_in_profile()
                    target_member.assign_member_perm()
                else:
                    target_member.create_personal_archive()
                    target_member.join_task_in_profile()
                    target_member.assign_member_perm()

                # 通知

            # 配置新增组长
            for each in new_leaders:
                try:
                    target_member.user_buildin = User.objects.get(id = each)
                    target_member.user_profile = UserProfile.objects.get(user_id = each)
                except UserProfile.DoesNotExist:
                    continue
                except User.DoesNotExist:
                    continue

                target_member.set_leader_in_profile()
                target_member.assign_leader_perm()

                # 通知

            return JsonResponse({"url": "/task/task_page/%d"%self.task.id, "status": 302}, safe=False)
        return JsonResponse({"tip": "表单验证失败", "status": 400}, safe=False)

    def delete_task(self, request):
        members = json.loads(self.task.members)
        leaders = json.loads(self.task.leaders)

        # 获取用户组
        target_group = Group.objects.get(name = str(self.task.id))
        target_group_leader = Group.objects.get(name = "%s%s"%(str(self.task.id), "leaders"))

        # 建立成员类
        target_member = member(target_task = self.task, target_group = target_group, target_group_leader = target_group_leader)

        # 撤销创建者的相关权限
        try:
            target_member.user_buildin = request.user
            target_member.user_profile = UserProfile.objects.get(user_id = request.user.id)
        except UserProfile.DoesNotExist:
            pass

        # 撤销组长
        for each in leaders:
            try:
                target_member.user_buildin = User.objects.get(id = each)
                target_member.user_profile = UserProfile.objects.get(user_id = each)
            except UserProfile.DoesNotExist:
                continue
            except User.DoesNotExist:
                continue

            target_member.cancel_leader_in_profile()
            target_member.remove_leader_perm()

        # 组员退出
        for each in members:
            try:
                target_member.user_buildin = User.objects.get(id = each)
                target_member.user_profile = UserProfile.objects.get(user_id = each)
            except UserProfile.DoesNotExist:
                continue
            except User.DoesNotExist:
                continue

            target_member.quit_task_in_profile()
            target_member.remove_member_perm()
            target_member.remove_archive_edit_perm()

        # 通知

        return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)

    def task_page(self, request):
        target_task = model_to_dict(self.task, fields=["id", "task_name", "publish_date", "deadline", "task_status", "members", "creator", "leaders", "task_description", "task_progress", "task_schedule", "task_comment", "appendixes"])
        target_task["publish_date"] = self.task.publish_date
        members = json.loads(target_task["members"])
        leaders = json.loads(target_task["leaders"])

        target_task["members"] = json.dumps([{**{"id": each}, **model_to_dict(UserProfile.objects.get(user_id = each), fields=['name', 'major'])} for each in members])
        target_task["leaders"] = json.dumps([{**{"id": each}, **model_to_dict(UserProfile.objects.get(user_id = each), fields=['name', 'major'])} for each in leaders])
        target_task["user_id"] = request.user.id
        target_task["task"] = self.task

        return render(request, "task_detail.html", target_task)

    @staticmethod
    def get_members(request):
        members = UserProfile.objects.filter(major=request.GET.get("key")) | UserProfile.objects.filter(name = request.GET.get("key"))
        members = members.values("name", "major", "user_id", "involved_projects_number", "managed_projects_number")
        
        return JsonResponse(list(members), safe=False)

class _publisher(object):
    detail = None

    def __init__(self, detail):
        self.detail = json.loads(detail)

    def upgrade(self, content, editor_id = 0):
        lastest = self.detail.pop()
        lastest["upgrade_date"] = str(time.time())
        lastest["content"] = content
        lastest["creater"] = editor_id
        self.detail.append(lastest)

        return json.dumps(self.detail)

    def create(self, content, editor_id = 0):
        self.detail.append({"publish_date": str(time.time()), "upgrade_date": str(time.time()), "content": content, "creater": editor_id})
        
        return json.dumps(self.detail)
