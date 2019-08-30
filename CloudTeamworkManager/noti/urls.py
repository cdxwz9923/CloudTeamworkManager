from django.urls import path
from . import views


urlpatterns = [
    path('delete_all_read/', views.delete_all_read),
    path('delete_target/<int:notification_id>', views.delete_target),
    path('get_read/', views.get_read),
    path('get_unread/', views.get_unread),
    path('mark_all_as_read/', views.mark_all_as_read),
    path('mark_target_as_read/<int:notification_id>/', views.mark_target_as_read),
    path('send_test/<int:type>', views.send_test),
    path('',views.notifications),
    path('get_target_type/<int:type>/', views.get_target_type),
]
