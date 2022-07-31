from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def home(request):
    return render(request, "home.html", {})

def signin(request):
    context = {}
    if request.method == "POST":
        email = request.POST.get("email")
        pswd  = request.POST.get("pswd")

        user = authenticate(request, username=email, password=pswd)

        next_page = request.scope.get("query_string", "").split(b"=")[-1].decode("utf-8") 
        if user:
            login(request, user)
            if next_page:
                return redirect(next_page, permanent=True)

            return redirect("/", permanent=True)

        return JsonResponse({
            "status": "loggin failed"
        })
        
    
    return render(request, "login.html", context)

def signout(request):
    logout(request)
    return JsonResponse({
        "status": "logged out successfully"
    })

    