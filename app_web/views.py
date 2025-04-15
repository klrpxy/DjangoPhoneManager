<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def login(request):
    return HttpResponse("login page")

>>>>>>> e643b94 (add funcion login and bind in urls)
