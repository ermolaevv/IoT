from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Telemetry, Devices
from django.forms.models import model_to_dict
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import login


@api_view(['GET', 'POST'])
def telemetry(request):
    url = request.get_full_path().split("?")[1]
    params = dict()

    for param in url.split("&"):
        name, value = param.split("=")
        params[name] = value


    if request.method == 'GET':
        print("GET", request.data)

        try:
            telemetry = Telemetry.objects.filter(token=params['token']).latest('ressived_time')
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(model_to_dict(telemetry), status=status.HTTP_200_OK)

    elif request.method == 'POST':
        print("POST", request.data)
        
        try:
            Devices.objects.get(token=params['token'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        telemetry = Telemetry.objects.create(
            token=token,
            received_time=timezone.now(),
            data=request.data
        )
        return Response(model_to_dict(telemetry), status=status.HTTP_200_OK)
    return Response(status=status.HTTP_418_IM_A_TEAPOT)

def index(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error_message': 'Неверное имя пользователя или пароль'})
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'register.html', {'error_message': 'Пароли не совпадают'})
    return render(request, 'register.html')