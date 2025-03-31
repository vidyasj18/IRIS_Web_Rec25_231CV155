from django.shortcuts import render
from infrastructure.models import Booking, WaitlistBooking, Notification

def custom_admin_dashboard(request):
    # Fetch all bookings
    bookings = Booking.objects.select_related('user', 'equipment').all().order_by('-request_date')

    # Fetch waitlist data
    waitlist = WaitlistBooking.objects.select_related('user', 'equipment').all().order_by('position')

    # Fetch admin notifications (e.g., new booking requests)
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'bookings': bookings,
        'waitlist': waitlist,
        'notifications': notifications
    }
    
    return render(request, 'admin_dashboard.html', context)
