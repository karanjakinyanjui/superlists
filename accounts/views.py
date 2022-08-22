import sys
from uuid import uuid4

from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
)
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from accounts.models import Token


def send_login_email(request):
    email = request.POST['email']
    uid = uuid4().hex
    Token.objects.create(email=email, uid=uid)
    print(f'Saving uid {uid} for email {email}', file=sys.stderr)
    url = request.build_absolute_uri(f'/accounts/login?token={uid}')
    send_mail(
        'Your login link for Superlists',
        f'Use this link to log in: \n\n{url}',
        'hugosnotif@gmail.com',
        [email]
    )
    return render(request, 'accounts/login_email_sent.html')


def login(request):
    print('login view', file=sys.stderr)
    uid = request.GET.get('token')
    user = authenticate(uid=uid)
    if user is not None:
        auth_login(request, user)
    return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect('/')