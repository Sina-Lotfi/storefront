from django.shortcuts import render

from .tasks import sina

def say_hell(request):
    sina.delay('hello')
    return render(request,'<h1>sina</h1>')