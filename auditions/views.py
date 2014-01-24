# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template import Context, loader
from sets import Set
import urllib, re

# Create your views here.

#from pce.models import Course, Course_Instance




# Adapted from Luke Paulsen's code.
def home(request):
    return HttpResponse("lol")
