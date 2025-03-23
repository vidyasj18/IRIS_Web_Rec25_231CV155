from django.shortcuts import render

# Create your views here.
from .models import Notification
from django.contrib.auth.decorators import login_required

# This will display the list of notifications to the user.
@login_required
def notifications_list(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications/notifications_list.html', {'notifications': user_notifications})

