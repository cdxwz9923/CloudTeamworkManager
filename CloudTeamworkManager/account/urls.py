from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page),
    path('logout/', views.logoutAccount),
    path('register/', views.register_page),
    path('reset_password/', views.reset_password_page),
    path('set_password/', views.set_password),
    path('check_phone_number/', views.check_phone_number),
    path('sendmsgcode/', views.sendmsgcode),
    path('space/', views.space_page),
    path('', views.home),
    path('perfect_information/', views.perfect_info),
    path('change_information/', views.change_info),
    path('task_list/', views.task_list),
]
