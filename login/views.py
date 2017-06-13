# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate
from django.contrib.auth.views import logout, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from login.forms.login import LoginForm
from login.forms.request import RequestForm
import sms

def login_user(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    result = {"ip": ip}

    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                # Redirect to a success page.
                if user.is_active:
                    login(request, user)
                    print "login sucess"
                    #return redirect('request')
                    return render(request, 'request.html')
                else:
                    result["login_error"] = 'Your account has been disabled.'
                    return render(request, 'login.html', result)
            else:
                result["login_error"] = 'Invalid login details.'
                return render(request, 'login.html', result)
        else:
            result["form"] = form
            return render(request, 'login.html', result)

    # Send login form.
    else:
        context = {"ip": ip}
        return render(request, 'login.html', context)


def process_request(request):

    print "request form is loaded"

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    result = {"ip": ip}

    if request.method == 'POST':
        form = RequestForm(data=request.POST)

        if form.is_valid():
            mobileno = form.cleaned_data['mobileno']
            message  = form.cleaned_data['message']

            ACCESS_TOKEN = sms.authenticate(ACCESS_TOKEN='')
            sms.send_msg(ACCESS_TOKEN,mobileno,message)

            print "Mobile No is:" + mobileno
            return render(request, 'request.html', result) 

def logout_user(request):

    logout(request)
    return HttpResponseRedirect(reverse("home"))

