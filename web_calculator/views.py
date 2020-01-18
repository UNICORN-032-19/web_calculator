from django.shortcuts import render
from datetime import datetime


def home(request):
    context = {'timestamp': datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")}
    return render(request, 'home.html', context)
