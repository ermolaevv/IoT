from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Telemetry, Devices
from django.forms.models import model_to_dict
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

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
            token= params['token'],
            ressived_time = timezone.now(),
            data = request.data
        )
        
        return Response(model_to_dict(telemetry), status=status.HTTP_200_OK)
    return Response(status=status.HTTP_418_IM_A_TEAPOT)

def index(request):
    return render(request,'index.html')