from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html', {"name": "Musab"});
# Create your views here.
def add(request):
    val1 = int(request.POST['one'])
    val2 = int(request.POST['two'])
    res = val1 + val2
    return render(request, 'result.html', {'result': res})