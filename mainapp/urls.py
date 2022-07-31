from unittest.mock import patch
from django.urls import path

from apis.views import complete_profile, create_eaxm
from .views import signin, signout, home

urlpatterns = [
    path("", home, name="home"),
    path("login/", signin, name="sign-in"),
    path("logout/", signout, name="sign-out"),
    path("complete_profile/", complete_profile, name="complete-profile"),
    path("create_exam/", create_eaxm, name="create-exam"),
]