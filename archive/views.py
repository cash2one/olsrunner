from django.shortcuts import render
from django.http import HttpResponse


def index(request):
	return HttpResponse("Hello, welcome to the ols archive, please choose a split to see statistics for it")
# Create your views here.
# Create your views here.
def splits(request, season, year):
	return HttpResponse("Season: ", season, " Year: ", year)