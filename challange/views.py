from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'index3.html')


def tbl(request):
    return render(request, 'pages/tables/simple.html')


def login(request):
    return render(request, 'login.html')

# TODO complete sendCode part
def sendCode(request):
    pass