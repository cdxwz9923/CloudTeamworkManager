from django.urls import path
from . import views

urlpatterns = [
    path('task_process/<int:task_id>', views.task_progress),
    path('task_comment/<int:task_id>', views.task_comment),
    path('task_shedule/<int:task_id>', views.task_shedule),
    path('personal_shedule/<int:task_id>/<int:member_id>', views.personal_shedule),
    path('personal_comments/<int:task_id>/<int:member_id>', views.personal_comments),
    path('personal_process/<int:task_id>/<int:member_id>', views.personal_progress),
    path('publisher/', views.publisher),
    ]
