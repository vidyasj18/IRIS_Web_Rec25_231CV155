# maps the registration  and login URL to the registration view.
from django.urls import path
from . import views

# added the function posts_list to the urlpatterns list
app_name = 'users'
urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
]

