from http.client import HTTPResponse
from django.http import HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="sign-in")
@ensure_csrf_cookie
def complete_profile(request):
    context = {}
    if request.user.is_authenticated:
        context["user"] = request.user
        context["csrftoken"] = request.COOKIES.get("csrftoken", "")
            
        return render(request, "complete-profile/index.html", context)
    
    return HTTPResponse("Unauthorized")


@login_required(login_url="sign-in")
@ensure_csrf_cookie
def create_eaxm(request):
    context = {}
    if request.user.is_authenticated:
        context["user"] = request.user
        context["csrftoken"] = request.COOKIES.get("csrftoken", "")

        return render(request, "create-exam/index.html", context)

    return HTTPResponse("Unauthorized")
