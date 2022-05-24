from django.shortcuts import render
from users.forms import UserLoginForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def loginUser(request):
    """
        Either render the form on a login page or triggers the login process
        if it receive a filled form
    """
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data['email'].lower())
            if user.count() == 0:
                messages.add_message(
                    request, messages.ERROR,
                    "The password or the email address is incorrect"
                )
            else:
                user = user.first()
                authuser = authenticate(username=user.username, password=form.cleaned_data['password'])
                if authuser:
                    login(request, authuser)
                    return HttpResponseRedirect(reverse('kitchen_display_view'))
                else:
                    messages.add_message(
                        request, messages.ERROR,
                        "The password or the email address is incorrect"
                    )
    messages.add_message(
        request, messages.ERROR,
        "Welcome to the NGUI Order Dispatcher Webiste ! This plateform is used by the restaurant owners. If you are not one of them, please leave."
    )
    form = UserLoginForm()
    view_title = "Login"
    return render(request, 'login.html', locals())


@login_required
def logout_view(request):
    """
        Logs the user out
    """
    logout(request)
    messages.add_message(
        request, messages.WARNING,
        "You have been disconnected !"
    )
    return HttpResponseRedirect(reverse('kitchen_display_view'))
