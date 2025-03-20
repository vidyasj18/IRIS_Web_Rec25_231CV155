from django.urls import path
from . import views

# added the function menu_list to the urlpatterns list
urlpatterns = [
    path('', views.posts_list ),
]