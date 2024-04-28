from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def telemetry(request):
    if request.method == 'GET':
        print("GET", request.data)
        return Response(request.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        print("POST", request.data)
        return Response(request.data, status=status.HTTP_200_OK)

def index(request):
    return render(request,'index.html')