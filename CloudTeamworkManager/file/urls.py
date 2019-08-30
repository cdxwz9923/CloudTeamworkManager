from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^picode/.*$', views.verify_code),
    path('image/<str:file_name>/', views.show_image),
    path('avatar/', views.avatar),
    path('appendix/<int:task_id>/<str:file_name>/', views.appendix),
    path('rename_appendix/<int:task_id>/<int:appendix_id>/', views.rename),
    path('delete_appendix/<int:task_id>/<int:appendix_id>/', views.delete),
    path('overlay_appendix/<int:task_id>/<int:appendix_id>/', views.overlay),
    path('appendix_list/<int:task_id>/', views.table),
]
