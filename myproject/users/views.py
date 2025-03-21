from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login

# Create your views here.
# creating a user registration feature
def register_view(request):
    # user clicks on menu(involves all posts uploaded by admin) button.
    if request.method == "POST": 
        form = UserCreationForm(request.POST)
        # user enters valid credentials. 
        if form.is_valid(): 
            login(request,form.save())
            return redirect("posts:list")
    else:
        form = UserCreationForm()
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

    