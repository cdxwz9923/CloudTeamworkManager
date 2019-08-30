from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.forms import ValidationError
from django.forms.models import model_to_dict
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm, LoginForm, ResetPasswordForm, extend_info, SetPasswordForm, my_clean_phone_number
from .forms import change_info as change_info_form
from .models import UserProfile
from .msgcode import sendcode
from task.models import task
import json


def logoutAccount(request):
    auth.logout(request)
    return HttpResponseRedirect("/account/login/")

def login_page(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        return render(request, 'signIn.html')

    if request.method == "POST":
        forms = LoginForm(request.POST)

        if forms.is_valid():
            user = auth.authenticate(request, username = forms.cleaned_data['phone_number'], password = forms.cleaned_data['password'])
            if user:
                auth.login(request, user)
                return JsonResponse({"url": "/", "status": 302}, safe=False)
            return JsonResponse({"tip": "用户名或密码错误", "status": 400}, safe=False)
        return JsonResponse({"tip": "输入内容有误", "status": 400}, safe=False)

    if request.method == "DELETE":
         auth.logout(request)
         return HttpResponseRedirect("/account/login/")

def register_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")

    if request.method == "GET":
        return render(request, 'signUp.html')

    if request.method == "POST":
        forms = RegisterForm(request.POST)

        if forms.is_valid():
            try:
                user = User.objects.get(username = forms.cleaned_data['phone_number'])
            except:
                user = User.objects.create_user(username = forms.cleaned_data['phone_number'], password=forms.cleaned_data['password'])
                UserProfile.objects.create(user_id = user.id)
                return JsonResponse({"url": "/account/login", "status": 302}, safe=False)
            return JsonResponse({"tip": "手机号已被注册", "status": 400}, safe=False)
        return JsonResponse({"tip": list(forms.errors.values())[0][0], "status": 400}, safe=False)

def reset_password_page(request):
    if request.method == "GET":
        return render(request, 'resetPassword.html')

    if request.method == "POST":
        forms = ResetPasswordForm(request.POST)

        if forms.is_valid():
            user = User.objects.get(username = forms.cleaned_data["phone_number"])
            user.set_password(forms.cleaned_data["password"])
            user.save()
            return JsonResponse({"url": "/account/login", "status": 302}, safe=False)
        return JsonResponse({"tip": list(forms.errors.values())[0][0], "status": 400}, safe=False)

@login_required
def set_password(request):
    if request.method == "GET":
        return render(request, 'setPassword.html')

    if request.method == "POST":
        forms = SetPasswordForm(request.POST)
        user = request.user  # 不用动这里
        forms.user = request.user  # 不用动这里
        forms.answer = request.session.get('verify').upper()

        if forms.is_valid():
            user.set_password(forms.cleaned_data["new_password"])
            auth.logout(request)
            return JsonResponse({"url": "/account/login", "status": 302}, safe=False)
        return JsonResponse({"tip": list(forms.errors.values())[0][0], "status": 400}, safe=False)

def check_phone_number(request):
    phone_number = request.POST.get("phone_number")

    try:
        my_clean_phone_number(phone_number)
    except ValidationError as e:
        return JsonResponse({"tip": e.message, "status": 400}, safe=False)
    return JsonResponse({"tip": "手机号码可用", "status": 200}, safe=False)

def sendmsgcode(request):
    def check_picode():
        answer = request.session.get('verify').upper()
        code = request.POST.get('picode').upper()

        if code == answer:
            auth.logout(request)
            return True
        return False

    if check_picode():
        sendcode(request.POST.get("phone_number"))
        return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
    return JsonResponse({"tip": "图形验证码校验失败", "status": 400}, safe=False)

@login_required
def space_page(request):
    target_userprofile = UserProfile.objects.get(user_id = request.user.id)
    target_user = request.user

    return render(request, 'space.html', {"name": target_userprofile.name, "phone_number": target_user.username, "gender": target_userprofile.sex, "student_id": target_userprofile.student_id, "birthday": target_userprofile.birthday, "email": target_userprofile.email, "major": target_userprofile.major, "grade": target_userprofile.grade, "room": target_userprofile.room, "home_address": target_userprofile.home_address, "guardian_phone": target_userprofile.guardian_phone, "introduction": target_userprofile.introduction, "user_id": target_user.id, "sex": target_userprofile.sex, "birthday": target_userprofile.birthday, "edit_status": "false", "edit_or_save": "编辑"})

def home(request):
    if request.user.is_authenticated:
        user_info = UserProfile.objects.get(user_id = request.user.id)

        if user_info.name:
            return render(request, 'home.html')
        return HttpResponseRedirect("/account/perfect_information/")
    return render(request, 'home.html')

@login_required
def personal_page(request):
    user_info = UserProfile.objects.get(user_id = request.user.id)
    involved_projects = json.loads(user_info["involved_projects"])
    projects_temp = []
    each_project_temp = {}
    for each_projects in involved_projects:
        task_id = each_projects
        task_status = task.objects.get(id = each_projects)["task_status"]
        each_project_temp["task_id"] = task_id
        each_project_temp["task_status"] = task_status
        projects_temp.append(each_project_temp)
    return render(request, "personal_page", {"user_info": user_info, "projects": projects_temp})

@login_required
def perfect_info(request):
    if request.method == "GET":
        return render(request, "perfect_info.html")

    if request.method == "POST":
        user_info = UserProfile.objects.get(user_id = request.user.id)
        if not user_info.name:
            forms = extend_info(request.POST, instance=user_info)

            if forms.is_valid():
                forms.save()
                return JsonResponse({"url": "/account/space/", "status": 302}, safe=False)
            return JsonResponse({"tip": list(forms.errors.values())[0][0], "status": 400}, safe=False)
        return JsonResponse({"tip": "权限不足", "status": 400}, safe=False)

@login_required
def change_info(request):
    if request.method == "GET":
        return render(request, "space.html", {"edit_status": "true", "edit_or_save": "保存"})

    if request.method == "POST":
        user_info = UserProfile.objects.get(user_id = request.user.id)
        forms = change_info_form(request.POST, instance=user_info)

        if forms.is_valid():
            forms.save()
            return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
        return JsonResponse({"tip": list(forms.errors.values())[0][0], "status": 400}, safe=False)

@login_required
def task_list(request):
    user = UserProfile.objects.get(user_id = request.user.id)
    _task_list = json.loads(user.involved_projects)
    temp = [task.objects.filter(id = each).values("id", "task_name", "members", "task_status")[0] for each in _task_list]
    for each_task in temp:
        members = json.loads(each_task["members"])
        each_task["members"] = [UserProfile.objects.get(user_id = each).name for each in members]
    return render(request, "task_list.html", {"content": temp, "name": user.name})
