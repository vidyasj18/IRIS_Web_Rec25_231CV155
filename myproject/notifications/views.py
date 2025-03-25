from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications_list(request):
    """ Fetch and display all notifications for the logged-in user """
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications/notifications_list.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    """ Marks a notification as read """
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications_list')

@login_required
def delete_notification(request, notification_id):
    """ Delete a notification """
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.delete()
    return redirect('notifications_list')

@login_required
def clear_all_notifications(request):
    """ Deletes all notifications for the logged-in user """
    Notification.objects.filter(user=request.user).delete()
    return redirect('notifications_list')
