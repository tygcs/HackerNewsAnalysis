from django.shortcuts import render, render_to_response
from django.http import HttpResponse


# Create your views here.

def test(request):
	content = {"a":1}
	return render_to_response('test.html', content);

