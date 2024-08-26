from django.shortcuts import render


# Create your views here.

def plate(request):
    return render(request, 'plate.html')