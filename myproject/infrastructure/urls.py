# all the URLs of infrastructure module are defined here.
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InfrastructureViewSet, BookingViewSet, WaitlistViewSet

router = DefaultRouter() # simplifies URL routing for APIs
# registers "InfrastructureViewSet" at /InfrastructureViewSet.
# users can view, add, update and admins can delete sports facilities.
router.register(r'infrastructures', InfrastructureViewSet)

# registers "BookingViewSet" at /BookingViewSet.
# users can book sports facilities and track their requests and even they can cancel as well.
router.register(r'bookings', BookingViewSet, basename='booking')
# router.register(r'waitlist', WaitlistViewSet, basename='waitlist')

urlpatterns = [
    path('', include(router.urls)),
]
