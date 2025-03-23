# implements the registration view, saving user details,
# and logging them in upon registration.
from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login


from django.contrib.auth import get_user_model
from django.http import JsonResponse

User = get_user_model()

def create_test_user(request):
    if User.objects.filter(username="testuser").exists():
        return JsonResponse({"error": "User already exists"}, status=400)

    user = User.objects.create_user(username="testuser", password="password123")
    return JsonResponse({"success": "User created"}, status=201)


# Create your views here.
# creating a user registration feature
def register_view(request):
    # user clicks on menu(involves all posts uploaded by admin) button.
    if request.method == "POST": 
        form = CustomUserCreationForm(request.POST)
        # user enters valid credentials. 
        if form.is_valid():
            user = form.save() 
            login(request,user)
            return redirect("posts:list")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", { "form": form })

def login_view(request):
    if request.method == "POST":
        # kwarg parameter is present, hence data should be passed inside.
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): 
            login(request, form.get_user())
            # log the user in
            return redirect("posts:list")
    
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

    