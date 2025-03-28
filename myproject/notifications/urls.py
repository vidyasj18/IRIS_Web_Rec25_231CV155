from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.notifications_list, name='notifications_list'),
    path('mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('clear-all/', views.clear_all_notifications, name='clear_all_notifications'),
    path('send/', views.send_notification, name='send_notification'),
]
