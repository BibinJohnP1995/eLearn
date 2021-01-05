from . models import *
import learn.views
from django.shortcuts import render

def logged_inn(function):
    def wrap(request):

        try:
            if request.session['logg']:
                return render(request, "admin_home.html")
        except:
            return render(request, "sama.html")

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
