from django.contrib import messages, auth
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse

from accounts.models import Token


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + f'?token={token.uid}'
    )
    send_mail(
        'Your login link for Superlists',
        f'Use this link to log in:\n\n{url}',
        'noreply@superlists',
        [email],
    )
    messages.add_message(
        request,
        messages.SUCCESS,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')


def login(request):
    token = request.GET.get("token")
    user = auth.authenticate(request, uid=token)
    if user:
        auth.login(request, user)
    return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/')
