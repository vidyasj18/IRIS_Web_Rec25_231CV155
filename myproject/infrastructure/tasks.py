from celery import shared_task
from django.utils.timezone import now
from .models import Booking, Notification
from datetime import timedelta
from celery.schedules import crontab
from celery import Celery

# used to send the reminder notification to the user before the booking starts.
@shared_task
def send_reminder_notifications():
    upcoming_bookings = Booking.objects.filter(start_time__lte=now() + timedelta(minutes=30))
    for booking in upcoming_bookings:
        message = f"Reminder: Your booking for {booking.infrastructure.name} starts in 30 minutes."
        Notification.objects.create(user=booking.user, message=message)

# Celery app configuration
app = Celery('myproject')

app.conf.beat_schedule = {
    'send-reminders-every-5-minutes': {
        'task': 'infrastructure.tasks.send_reminder_notifications',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
    },
}