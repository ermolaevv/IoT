from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Telemetry
from django.forms.models import model_to_dict
from django.utils import timezone

@api_view(['GET', 'POST'])
def telemetry(request):
    if request.method == 'GET':
        print("GET", request.data)
        return Response(request.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        print("POST", request.data)
        url = request.get_full_path().split("?")[1]
        params = dict()

        for param in url.split("&"):
            name, value = param.split("=")
            params[name] = value

        telemetry = Telemetry.objects.create(
            token= params['token'],
            ressived_time = timezone.now(),
            data = request.data
        )
        
        return Response(model_to_dict(telemetry), status=status.HTTP_200_OK)

def index(request):
    return render(request,'index.html')