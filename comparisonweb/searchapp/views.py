from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'searchapp/home.html')

def result(request):
    return render(request, 'searchapp/result.html')